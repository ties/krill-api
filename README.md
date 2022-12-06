# krill-api-py

Use the [NLnetlabs/krill](https://github.com/NLnetLabs/krill) API from python.

Make sure you set up the environment variables first before trying the
workbook:
```
export KRILL_TOKEN=...
export KRILL_URL='...'
# Dump the certificate in DER format like
# > openssl s_client -showcerts \
#     -servername krill.host \
#     -connect krill.host:3000 2>/dev/null | openssl x509 -inform pem -outform DER -out {KRILL_CERT_PATH}.der
export KRILL_CERT_PATH='...'

poetry run jupyter-lab
# And open the workbook to experiment
```
