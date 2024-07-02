
pip install -r requirements.txt

python manage.py collectstatic --no-input

cd BookRec_Server

expose 6000

docker build -t bookrec .
docker run -p 6000:6000 bookrec

cd ..
