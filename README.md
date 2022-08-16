### Взаимодействие с API VPBX MTS и S3
Скрипт забирает по API записи из витруальной АТС МТС и складывает их в S3 хранилище.

В каталоге со скриптом должен быть файл .env со следующими переменными:
```
VPBX_API_TOKEN=xxx-xxx-xxx
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
```