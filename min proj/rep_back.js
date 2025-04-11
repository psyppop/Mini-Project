const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
// Increase the JSON limit for larger payloads (signatures can be large)
app.use(bodyParser.json({ limit: '50mb' }));
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'rootsavio321', // Replace with your MySQL password
    database: 'reports'
});

db.connect((err) => {
    if (err) throw err;
    console.log('MySQL connected...');
});

// Handle JSON parsing errors
app.use((err, req, res, next) => {
    if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
        return res.status(400).json({ error: 'Invalid JSON payload' });
    }
    next();
});

app.post('/save-report', (req, res) => {
    const reportData = req.body;

    console.log('Received Report Data:', reportData); // Debugging: Log received data

    // Convert empty strings to null for date fields
    if (reportData.dateOfReport === '') reportData.dateOfReport = null;
    if (reportData.dateOfIncident === '') reportData.dateOfIncident = null;

    // Validate required fields
    if (!reportData.firNumber) {
        return res.status(400).json({ error: 'FIR Number is required.' });
    }

    // Check if statements is a string and parse it if needed
    if (typeof reportData.statements === 'string') {
        try {
            // Ensure statements is a valid JSON string
            reportData.statements = JSON.parse(reportData.statements);
        } catch (error) {
            console.error('Error parsing statements:', error);
            return res.status(400).json({ error: 'Invalid statements data.' });
        }
    }

    // Convert statements back to a string for storage
    if (Array.isArray(reportData.statements)) {
        reportData.statements = JSON.stringify(reportData.statements);
    }

    // Check if the report already exists
    const checkSql = 'SELECT * FROM reports WHERE firNumber = ?';
    db.query(checkSql, [reportData.firNumber], (err, result) => {
        if (err) {
            console.error('Error checking report:', err);
            return res.status(500).json({ error: 'Failed to check report.' });
        }
        
        if (result.length > 0) {
            // Update existing report
            const updateSql = 'UPDATE reports SET ? WHERE firNumber = ?';
            db.query(updateSql, [reportData, reportData.firNumber], (err, result) => {
                if (err) {
                    console.error('Error updating report:', err);
                    return res.status(500).json({ error: 'Failed to update report.' });
                }
                res.json({ message: 'Report updated successfully' });
            });
        } else {
            // Insert new report
            const insertSql = 'INSERT INTO reports SET ?';
            db.query(insertSql, reportData, (err, result) => {
                if (err) {
                    console.error('Error saving report:', err);
                    return res.status(500).json({ error: 'Failed to save report.' });
                }
                res.json({ message: 'Report saved successfully' });
            });
        }
    });
});

app.get('/get-report/:firNumber', (req, res) => {
    const firNumber = req.params.firNumber;
    const sql = 'SELECT * FROM reports WHERE firNumber = ?';
    db.query(sql, [firNumber], (err, result) => {
        if (err) {
            console.error('Error retrieving report:', err);
            return res.status(500).json({ error: 'Failed to retrieve report.' });
        }
        
        if (result.length > 0) {
            // Parse statements back to object if it's a string
            const report = result[0];
            if (typeof report.statements === 'string') {
                try {
                    report.statements = JSON.parse(report.statements);
                } catch (error) {
                    console.error('Error parsing stored statements:', error);
                    report.statements = [];
                }
            }
            res.json(report);
        } else {
            res.status(404).json({ error: 'Report not found' });
        }
    });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));