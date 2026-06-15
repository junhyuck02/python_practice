def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w")
    file.write("Title,Company,Career,Reward,Link\n")

    for job in jobs:
        file.write(
            f"{job['title']},{job['company_name']}, {job['career']}, {job['reward']}, {job['link']}\n"
        )

    file.close()
