Se ricevo messaggio `Address already in use`
```bash
sudo lsof -nti:PORT_NUMBER | killargs -9
```
sostituendo `PORT_NUMBER` con il numero di porta che si vuole liberare