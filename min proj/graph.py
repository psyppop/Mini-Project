import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import RadioButtons

class graph:
    def __init__(self):
        self.prepare_data()
        self.setup_ui()
        

    def prepare_data(self):
        sns.set_style("whitegrid")
        np.random.seed(42)
        self.years = list(range(2020, 2026))
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.locations = ['Nerul', 'Vashi', 'Kharghar']
        self.crimes = ['Theft', 'Assault', 'Burglary']
        
        self.data = []
        for year in self.years:
            for month in self.months:
                for location in self.locations:
                    self.data.append({
                        'Year': year,
                        'Month': month,
                        'Location': location,
                        'Theft': np.random.randint(20, 100),
                        'Assault': np.random.randint(10, 50),
                        'Burglary': np.random.randint(5, 30)
                    })
        self.df = pd.DataFrame(self.data)

    def setup_ui(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 9))
        self.fig.suptitle("Crime Statistics Overview", fontsize=16, fontweight="bold")
        plt.subplots_adjust(left=0.3, hspace=0.5, wspace=0.4)
        self.ax_radio = plt.axes([0.05, 0.2, 0.15, 0.4])
        self.radio = RadioButtons(self.ax_radio, [str(year) for year in self.years])
        self.radio.on_clicked(self.update)
        self.selected_year = 2025
        self.update(str(self.selected_year))

    def update(self, year_label):
        self.selected_year = int(year_label)
        filtered_df = self.df[self.df["Year"] == self.selected_year]
        
        for ax in self.axes.flatten():
            ax.clear()

        monthly_crimes = filtered_df.groupby('Month')[self.crimes].mean()
        monthly_crimes.plot(marker='o', ax=self.axes[0, 0], linewidth=2)
        self.axes[0, 0].set_title(f'Monthly Crime Trends ({self.selected_year})')
        self.axes[0, 0].set_ylabel('Incidents')
        self.axes[0, 0].set_xticks(range(len(self.months)))
        self.axes[0, 0].set_xticklabels(self.months, rotation=45)

        location_crimes = filtered_df.groupby('Location')[self.crimes].mean()
        location_crimes.plot(kind='bar', ax=self.axes[0, 1], colormap='viridis', width=0.7)
        self.axes[0, 1].set_title(f'Crime by Location ({self.selected_year})')
        self.axes[0, 1].set_ylabel('Incidents')
        self.axes[0, 1].set_xticklabels(self.locations, rotation=20, ha='right')

        total_crimes = filtered_df[self.crimes].sum()
        self.axes[1, 0].pie(total_crimes, labels=self.crimes, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
        self.axes[1, 0].set_title(f'Crime Type Distribution ({self.selected_year})')

        yearly_crimes = self.df.groupby('Year')[self.crimes].mean()
        yearly_crimes.plot(kind='bar', ax=self.axes[1, 1], width=0.6, colormap='coolwarm')
        self.axes[1, 1].set_title('Yearly Crime Comparison')
        self.axes[1, 1].set_ylabel('Incidents')
        self.axes[1, 1].set_xticklabels(self.df["Year"].unique(), rotation=0)

        self.fig.canvas.draw_idle()

    def generate_graph(self):
        plt.show()

if __name__ == "__main__":
    graph_instance = graph()
    graph_instance.generate_graph()