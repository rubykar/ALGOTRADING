import tkinter as tk
from tkinter import filedialog
import pandas as pd

from functions import (
    find_close_rsi,
    find_next_hour_open,
    get_close_day0,
    get_next_close_day1,
    get_next_close_day2,
    get_next_close_day3,
)


class CSVViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Viewer")
        self.create_widgets()
        self.root.columnconfigure(0, weight=1)

    def create_widgets(self):
        # File selection widgets
        self.file_label = tk.Label(self.root, text="Upload CSV File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=5)

        self.file_entry = tk.Entry(self.root, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(
            self.root, text="Browse", command=self.upload_file
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Options
        self.options_label = tk.Label(self.root, text="Options:")
        self.options_label.grid(row=1, column=0, padx=10, pady=5)

        self.close_checkbox = tk.Checkbutton(
            self.root, text="Close", variable=tk.BooleanVar()
        )
        self.close_checkbox.grid(row=1, column=1, padx=5, pady=5)
        self.close_checkbox = tk.Checkbutton(
            self.root, text="Rsi", variable=tk.BooleanVar()
        )
        self.close_checkbox.grid(row=1, column=2, padx=5, pady=5)

        # Display button
        self.display_button = tk.Button(
            self.root, text="Display File", command=self.display_file
        )
        self.display_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.text_display = tk.Text(self.root, wrap=tk.WORD)
        self.text_display.grid(
            row=3, column=0, columnspan=3, padx=12, pady=5, sticky="nsew"
        )

        # Scrollbar
        scrollbar = tk.Scrollbar(
            self.root, orient=tk.VERTICAL, command=self.text_display.yview
        )
        scrollbar.grid(row=3, column=4, sticky="ns")
        self.text_display.config(yscrollcommand=scrollbar.set)

        self.download_button = tk.Button(
            self.root, text="Download CSV", command=self.download_csv
        )
        self.download_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def display_file(self):
        file_path = self.file_entry.get()
        data = pd.read_csv("hourlyData.csv")
        data = self.format_date_hourly(data)
        data = data[
            ["Symbol", "date_only", "time_only", "Close", "Open", "High", "RSI"]
        ]
        grouped_df = data.groupby("Symbol")
        data["ema"] = grouped_df["Close"].transform(
            lambda x: x.ewm(span=20, adjust=False, min_periods=20).mean()
        )
        data["ema50"] = grouped_df["Close"].transform(
            lambda x: x.ewm(span=50, adjust=False, min_periods=50).mean()
        )
        data["sma"] = grouped_df["Close"].transform(
            lambda x: x.rolling(window=200).mean()
        )

        result_df = pd.read_csv("DailyNifty500.csv")

        if file_path:
            try:
                df = pd.read_csv(file_path)
                formatted_df = self.format_date(df)
                formatted_df = formatted_df[["symbol", "DATE", "TIME"]]
                formatted_df["close"], formatted_df["rsi"], formatted_df["high"] = zip(
                    *formatted_df.apply(
                        lambda row: find_close_rsi(
                            row["symbol"],
                            row["DATE"],
                            row["TIME"],
                            data_6m_hourly=data,
                        ),
                        axis=1,
                    )
                )
                formatted_df["next_hour_open"] = formatted_df.apply(
                    lambda row: find_next_hour_open(
                        row["symbol"], row["DATE"], row["TIME"], data_6m_hourly=data
                    ),
                    axis=1,
                )
                formatted_df["close_price_day0"] = formatted_df.apply(
                    lambda row: get_close_day0(row["symbol"], row["DATE"], result_df),
                    axis=1,
                )
                formatted_df["next_close_day1"] = formatted_df.apply(
                    lambda row: get_next_close_day1(
                        row["symbol"], row["DATE"], result_df
                    ),
                    axis=1,
                )
                formatted_df["next_close_day2"] = formatted_df.apply(
                    lambda row: get_next_close_day2(
                        row["symbol"], row["DATE"], result_df
                    ),
                    axis=1,
                )
                formatted_df["next_close_day3"] = formatted_df.apply(
                    lambda row: get_next_close_day3(
                        row["symbol"], row["DATE"], result_df
                    ),
                    axis=1,
                )
                self.formatted_df = formatted_df
                self.text_display.insert(tk.END, formatted_df.to_string(index=False))
            except Exception as e:
                self.text_display.insert(tk.END, "Error reading file: " + str(e))
        else:
            self.text_display.insert(tk.END, "Please upload a CSV file.")

    def format_date_hourly(self, data):
        data["Date"] = pd.to_datetime(data["Date"])

        data["date_only"] = data["Date"].dt.date
        data["time_only"] = data["Date"].dt.time

        data.drop(columns=["Date"], inplace=True)

        return data

    def format_date(self, dataframe):
        dataframe["date"] = pd.to_datetime(
            dataframe["date"], format="%d-%m-%Y %I:%M %p"
        )
        dataframe["DATE"] = dataframe["date"].dt.date
        dataframe["TIME"] = dataframe["date"].dt.time

        return dataframe

    def download_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
            )

            # Save the DataFrame to CSV
            self.formatted_df.to_csv(file_path, index=False)

            # Close the application
            self.root.destroy()

        except Exception as e:
            # Handle any errors
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewer(root)
    root.mainloop()
