import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from a CSV file (you can replace this with your file)
data_file = "weather_data.csv"
data = pd.read_csv(data_file)

# Analyze the data
summary = {
    "Temperature": {
        "Average": data["Temperature (°C)"].mean(),
        "Max": data["Temperature (°C)"].max(),
        "Min": data["Temperature (°C)"].min(),
    },
    "Humidity": {
        "Average": data["Humidity (%)"].mean(),
        "Max": data["Humidity (%)"].max(),
        "Min": data["Humidity (%)"].min(),
    },
}

# Create visualizations
sns.set(style="whitegrid")

# Temperature plot
plt.figure(figsize=(8, 5))
sns.barplot(x="City", y="Temperature (°C)", data=data, palette="coolwarm")
plt.title("Temperature Comparison")
plt.tight_layout()
plt.savefig("temperature_plot.png")
plt.close()

# Humidity plot
plt.figure(figsize=(8, 5))
sns.barplot(x="City", y="Humidity (%)", data=data, palette="Blues")
plt.title("Humidity Comparison")
plt.tight_layout()
plt.savefig("humidity_plot.png")
plt.close()

# Generate PDF report
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", style="B", size=12)
        self.cell(0, 10, "Weather Data Analysis Report", border=False, ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = PDFReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Add summary to the PDF
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, "Summary of Weather Data:", ln=True)

for key, values in summary.items():
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, f"{key}:", ln=True)
    pdf.set_font("Arial", size=10)
    for stat, value in values.items():
        pdf.cell(0, 10, f"  {stat}: {value:.2f}", ln=True)

# Add visualizations to the PDF
pdf.add_page()
pdf.cell(0, 10, "Temperature Plot:", ln=True)
pdf.image("temperature_plot.png", x=10, y=30, w=190)

pdf.add_page()
pdf.cell(0, 10, "Humidity Plot:", ln=True)
pdf.image("humidity_plot.png", x=10, y=30, w=190)

# Save the PDF
pdf.output("weather_report.pdf")

print("Task completed! Report saved as 'weather_report.pdf'.")