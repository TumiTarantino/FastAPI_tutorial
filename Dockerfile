FROM  python:3.12-slim-bookworm
#Docker's working directory
WORKDIR /usr/src/app
#This is makes it so changing the requirements runs everything below this line con...
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#first . is copy from, second . is copy to
#...tinued, but changing anything else only runs from here
COPY . .
#Usual command, just split whitespace/args
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]