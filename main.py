import os
import json
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT


# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Input file
input_file = "student_enrollment_raw.csv"

# Read CSV
df = pd.read_csv(input_file)

print("Total students:", len(df))

# Get first student
student = df.iloc[0].to_dict()

print("\nOriginal student:")
print(student)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": json.dumps(student)
        }
    ]
)

cleaned_student = json.loads(
    response.choices[0].message.content
)

print("\nCleaned student:")
print(cleaned_student)

cleaned_students = []

for index, row in df.iterrows():

    student = row.to_dict()

    print(f"Processing student {index + 1}/{len(df)}...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(student)
            }
        ]
    )

    cleaned_student = json.loads(
        response.choices[0].message.content
    )

    cleaned_students.append(cleaned_student)

print("\nAll students processed.")

cleaned_df = pd.DataFrame(cleaned_students)

output_file = "output/student_enrollment_cleaned.csv"

cleaned_df.to_csv(
    output_file,
    index=False
)

print(f"\nFinal file created: {output_file}")