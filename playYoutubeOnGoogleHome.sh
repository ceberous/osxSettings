#!/bin/bash
# Quick Find MacAddress
# python3
# import pychromecast
# pychromecast.get_chromecasts()
# arp -na
MacAddress="f4:f5:d8:d8:e5:f4"
ChromecastIP=$(arp -na | grep -i $MacAddress | tail -1 | awk '{print $2}' | cut -d "(" -f2 | cut -d ")" -f1)
if [ -z "$ChromecastIP" ]; then
	echo "arp scan empty"
	if [[ "$OSTYPE" == "linux-gnu" ]]; then
		DefaultGateway=$(netstat -rn -A inet | grep -A 1 "Gateway" | tail -1 | awk '{print $2}')
	elif [[ "$OSTYPE" == "darwin"* ]]; then
		DefaultGateway=$(ip route ls | grep default | awk '{print $3}')
	fi
	echo "Default Gateway = $DefaultGateway"
	echo "nmaping Default Gateway ..."
	ChromecastIP=$(sudo nmap -sn $DefaultGateway/24 | grep -i '$MacAddress' -B 2 | head -1 | awk '{print $(NF)}')
fi
if [ -z "$ChromecastIP" ]; then
	ChromecastIP=$(arp -na | grep -i $MacAddress | tail -1 | awk '{print $2}' | cut -d "(" -f2 | cut -d ")" -f1)
fi
echo "ChromecastIP = $ChromecastIP"
DirectURL=$(youtube-dl --no-warnings -f "best" --no-playlist --get-url $1)
echo $DirectURL
node -e 'const process=require("process");const path=require("path");const global_package_path=process.argv[0].split("/bin/node")[0]+"/lib/node_modules";const Client=require(path.join(global_package_path,"castv2-client")).Client;const DefaultMediaReceiver=require(path.join(global_package_path,"castv2-client")).DefaultMediaReceiver;let GoogleHomeClient;function CONNECT(google_home_ip){return new Promise((resolve,reject)=>{try{if(!google_home_ip){resolve(false);return false}GoogleHomeClient=new Client();GoogleHomeClient.connect(google_home_ip,()=>{console.log("connected to google home");resolve();return})}catch(error){console.log(error);reject(error);return}})}function PLAY_HOSTED_MP3(direct_mp3_url){return new Promise((resolve,reject)=>{try{GoogleHomeClient.launch(DefaultMediaReceiver,(err,player)=>{const media_mp3={contentId:direct_mp3_url,contentType:"audio/mp3",streamType:"BUFFERED"};player.on("status",(status)=>{if(status){if(status.playerState){console.log(status.playerState);if(status.playerState==="PLAYING"){resolve();return}}}});player.load(media_mp3,{autoplay:true},(error,status)=>{if(status){const two=1+1}})})}catch(error){console.log(error);reject(error);return}})}(async()=>{const google_home_ip=process.argv[1];const direct_mp3_url=process.argv[2];await CONNECT(google_home_ip);await PLAY_HOSTED_MP3(direct_mp3_url);return})();' "$ChromecastIP" "$DirectURL"