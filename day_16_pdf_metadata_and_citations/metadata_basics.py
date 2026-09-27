



chunks = [
    {
        "text": "Employees receive 20 days of annual leave.",
        "source": "employee_handbook.pdf",
        "page": 17
    },
    {
        "text": "Travel expenses must be submitted within 30 days.",
        "source": "travel_policy.pdf",
        "page": 4
    }
]

for chunk in chunks:
    print("text: ",chunk["text"])
    print("source: ",chunk["source"])
    print("page: ",chunk["page"])
    print()
