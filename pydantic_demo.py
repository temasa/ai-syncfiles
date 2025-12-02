from pydantic import BaseModel
from datetime import datetime

class FileWithDate(BaseModel):
    filename: str
    created_date: datetime


def main():
    file1 = FileWithDate(filename="a", created_date=datetime.now())
    file2 = FileWithDate(filename="b", created_date=datetime.now())

    print(file1, file2)



if __name__ == "__main__":
    main()