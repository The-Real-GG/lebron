import pandas as pd

CSV_FILENAME = "Tompkins Students - LeBron James Knowledge Survey (Responses) - Sheet1.csv"

def fmt(count, denom):
    pct = (count / denom * 100) if denom > 0 else 0
    return f"{pct:.2f}% ({count}/{denom})"

def choose_index(prompt, max_idx):
    while True:
        try:
            i = int(input(prompt).strip())
            if 0 <= i < max_idx:
                return i
            print(f"Enter a number between 0 and {max_idx - 1}.")
        except ValueError:
            print("Invalid number. Try again.")

def load_clean_csv():
    df = pd.read_csv(CSV_FILENAME)

    # Clean columns, strip whitespace, normalize "nan"
    df.columns = [str(c).strip() for c in df.columns]
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).str.strip().replace({"nan": None})

    return df

def main():
    print("\nLoading CSV file...")
    df = load_clean_csv()
    total = len(df)
    print(f"Loaded {CSV_FILENAME} with {total} rows.\n")

    # Show available categories
    print("Available categories (columns):")
    for i, col in enumerate(df.columns):
        print(f"  [{i}] {col}")

    # Category 1
    idx1 = choose_index("\nChoose Category 1 index: ", len(df.columns))
    cat1 = df.columns[idx1]

    vals1 = list(df[cat1].dropna().unique())
    print(f"\nResponses for '{cat1}':")
    for i, v in enumerate(vals1):
        print(f"  ({i}) {v}")
    idx_val1 = choose_index("Choose response index for Category 1: ", len(vals1))
    val1 = vals1[idx_val1]

    # Relation Type
    while True:
        rel = input("\nEnter relation ('Given', 'And', 'OnlyCategory1'): ").strip().lower()
        if rel in ["given", "and", "onlycategory1"]:
            break
        print("Invalid. Must be: Given / And / OnlyCategory1")



    if rel == "and":
        idx2 = choose_index("\nChoose Category 2 index: ", len(df.columns))
        cat2 = df.columns[idx2]

        vals2 = list(df[cat2].dropna().unique())
        print(f"\nResponses for '{cat2}':")
        for i, v in enumerate(vals2):
            print(f"  ({i}) {v}")
        idx_val2 = choose_index("Choose response index for Category 2: ", len(vals2))
        val2 = vals2[idx_val2]

        # Compute
        cond1 = df[cat1] == val1
        cond2 = df[cat2] == val2

        count1 = cond1.sum()
        count2 = cond2.sum()
        joint = (cond1 & cond2).sum()

        print("\n=== RESULTS ===\n")

        print(f"P({cat1} = {val1} AND {cat2} = {val2}) = {fmt(joint, total)}")

    elif rel == "given":

        idx2 = choose_index("\nChoose Category 2 index: ", len(df.columns))
        cat2 = df.columns[idx2]

        vals2 = list(df[cat2].dropna().unique())
        print(f"\nResponses for '{cat2}':")
        for i, v in enumerate(vals2):
            print(f"  ({i}) {v}")
        idx_val2 = choose_index("Choose response index for Category 2: ", len(vals2))
        val2 = vals2[idx_val2]

        # Compute
        cond1 = df[cat1] == val1
        cond2 = df[cat2] == val2

        count1 = cond1.sum()
        count2 = cond2.sum()
        joint = (cond1 & cond2).sum()

        print("\n=== RESULTS ===\n")

        print(f"P({cat1} = {val1} AND {cat2} = {val2}) = {fmt(joint, total)}")
        if count2 == 0:
            print(f"P({cat1} | {cat2}) cannot be computed (zero matching rows).")
        else:
            print(f"P({cat1} = {val1} | {cat2} = {val2}) = {fmt(joint, count2)}")

    else:  # OnlyCategory1
        cond1 = df[cat1] == val1
        count1 = cond1.sum()

        print("\n=== RESULTS ===\n")

        print(f"P({cat1} = {val1}) = {fmt(count1, total)}")
        print(f"P({cat1} != {val1}) = {fmt(total - count1, total)}")

    print("\nDone.\n")

if __name__ == "__main__":
    main()
