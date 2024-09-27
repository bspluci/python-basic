file = open("member.csv", "w", encoding="utf-8-sig")
file.write("이름, 나이, 성별, 이메일, 전화번호\n")
file.close()

member_data = [
    {
        "name": "김철수",
        "age": 20,
        "sex": "남",
        "email": "abcd@naver.com",
        "phone": "010-1234-5678",
    },
    {
        "name": "이영희",
        "age": 25,
        "sex": "여",
        "email": "efg@hanmail.net",
        "phone": "010-9876-5432",
    },
    {
        "name": "박민수",
        "age": 30,
        "sex": "남",
        "email": "hijk@gmail.com",
        "phone": "010-5678-1234",
    },
]

file = open("member.csv", "a", encoding="utf-8-sig")
for index, member in enumerate(member_data):
    file.write(
        f'{member["name"]}, {member["age"]}, {member["sex"]},'
        f'{member["email"]}, {member["phone"]}\n'
    )
file.close()

file = open("member.csv", "r", encoding="utf-8-sig")
print(file.read())
file.close()


testList = member_data[0].items()
for item in testList:
    print(f"{item[0]} = {item[1]},")
