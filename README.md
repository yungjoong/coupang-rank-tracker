## 환경설정 확인

```bash
git config --get pull.rebase
git config --global --get pull.rebase

# False 가 나와야 함. 아니라면

git config --global pull.rebase false
git config pull.rebase false
```