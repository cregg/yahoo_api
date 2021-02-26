docker run -t -i -p 5000:5000 -w /app --env-file app/dev.txt -v ${PWD}/app:/app yahoo sh -c "py.test"
