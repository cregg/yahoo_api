docker run -t -i -p 5000:5000 -w /app --env-file dev.txt -v ${PWD}:/app yahoo sh -c "flask run --host=0.0.0.0"
