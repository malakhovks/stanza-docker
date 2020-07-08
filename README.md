# stanza-docker
**Stanza** library inside docker container demo (Norwegian Bokmaal model load inside at first app start).

- clone project;
- build docker image: `docker build . -t stanza-image`;
- run container: `docker run --name stanza -d -p 45101:80 stanza-image`;
- POST request to `http://127.0.0.1:45101/test/message` with JSON `{'message': 'Formuesskatten er en skatt som utlignes på grunnlag av nettoformuen din.'}`