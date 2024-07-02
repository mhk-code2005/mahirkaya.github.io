
pip install -r requirements.txt

cd BookRec_Server


docker build -t bookrec .
docker run -p 6000:6000 bookrec

cd ..


python manage.py collectstatic --no-input

