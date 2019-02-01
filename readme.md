# Barcode reader server

This server reads from a stream from the pi zero.

It then looks for a barcode and if found sends it to
the main control server as a json payload.

The frame rate has been throttled to about 2 frames per second to make it
respond in a timely fashion, this is done by just reading the stream, frames
and throwing them away, then just process every 13th frame.

The output is just an endpoint on your webserver http://YOUR-IP-ADDRESS:5003/video_feed
and you may need to change the ip address in the server.py
file to your boxes ip address.

## Installation

instructions assumes you already have numpy and openCv installed on your server.

You may need pip instead

```bash
sudo apt-get install libzbar0

pip3 install -r requirements.txt

```

## Running the app

Now run where:

-W is the ip of the main websocket server
-V is the ip of the main video feed.

```bash
python3 ./server.py -W "192.168.55.13:5001" -V "192.168.255.12:8081"
```

You can now view it in the dashboard app by adding a new feed in 'Settings'

NOTE: The barcode must be a valid Dictionary object.
