import customtkinter as ctk
import json
from app.core.deepdiff_comparator import compareJson, diff_parser

def launch_app(): 

    # ======================
    # LOGIC
    # ======================
    def compare():
        try:
            before_json = json.loads(before_text.get("1.0", "end").strip())
            after_json = json.loads(after_text.get("1.0", "end").strip())

            diff_result = compareJson(before_json, after_json)
            diff_parsed = json.dumps(
                diff_parser(diff_result),
                indent=4,
                ensure_ascii=False,
                default=str
            )

            result_text.configure(state="normal")
            result_text.delete("1.0", "end")
            result_text.insert("end", diff_parsed)
            result_text.configure(state="disabled")

        except Exception as e:
            result_text.configure(state="normal")
            result_text.delete("1.0", "end")
            result_text.insert("end", f"Error: {e}")
            result_text.configure(state="disabled")


    # ======================
    # APP SETUP
    # ======================
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("JSON Diff Tool")
    app.geometry("800x600")


    # ======================
    # TITLE
    # ======================
    title = ctk.CTkLabel(app, text="JSON Comparator", font=("Arial", 22, "bold"))
    title.pack(pady=15)


    # ======================
    # MAIN CONTAINER
    # ======================
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)


    # ======================
    # TEXT FRAME
    # ======================
    text_frame = ctk.CTkFrame(frame)
    text_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    text_frame.grid_rowconfigure(1, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)
    text_frame.grid_columnconfigure(1, weight=1)


    # ======================
    # BEFORE
    # ======================
    before_label = ctk.CTkLabel(text_frame, text="Before JSON")
    before_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    before_text = ctk.CTkTextbox(text_frame)
    before_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


    # ======================
    # AFTER
    # ======================
    after_label = ctk.CTkLabel(text_frame, text="After JSON")
    after_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    after_text = ctk.CTkTextbox(text_frame)
    after_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


    # ======================
    # BUTTON
    # ======================
    compare_button = ctk.CTkButton(frame, text="Compare", command=compare)
    compare_button.grid(row=1, column=0, pady=10, padx=20, sticky="ew")


    # ======================
    # RESULT
    # ======================
    result_label = ctk.CTkLabel(frame, text="Result")
    result_label.grid(row=2, column=0, sticky="w", padx=20)

    result_text = ctk.CTkTextbox(frame)
    result_text.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
    result_text.configure(state="disabled")


    frame.grid_rowconfigure(3, weight=1)


    # ======================
    # RUN
    # ======================
    app.mainloop()