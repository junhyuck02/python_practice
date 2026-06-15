from extractors.wanted import extract_wanted_jobs
from file import save_to_file

keyword = input("What do you want to search for?")

jobs = extract_wanted_jobs(keyword)

save_to_file(keyword, jobs)
