import json, os, base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class PasswordVault:
    def __init__(self, MasterPassword):
        self.MasterPassword = MasterPassword.encode()
        self.Salt = None
        self.Fernet = None

        self.PasswordRecords = []
        self.VaultFilePath = f"{os.getcwd()}/Data/Vault.json"
        self.LoadVault()

    def DeriveKey(self):
        # Derive a 32-byte key from the given password and salt using PBKDF2
        return base64.urlsafe_b64encode(
            PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.Salt,
                iterations=100000,
            ).derive(self.MasterPassword)
        )

    def LoadVault(self):
        if os.path.exists(self.VaultFilePath):
            with open(self.VaultFilePath, "r") as File:
                VaultJson = json.load(File)

            self.Salt = base64.b64decode(VaultJson["Salt"])
            self.Fernet = Fernet(self.DeriveKey())

            self.PasswordRecords = []

            for PasswordRecord in VaultJson.get("Records", []):
                self.PasswordRecords.append({
                    "SiteName": self.Fernet.decrypt(PasswordRecord["SiteName"].encode()).decode(),
                    "Comment": self.Fernet.decrypt(PasswordRecord["Comment"].encode()).decode(),
                    "Username": self.Fernet.decrypt(PasswordRecord["Username"].encode()).decode(),
                    "Password": self.Fernet.decrypt(PasswordRecord["Password"].encode()).decode(),
                })

        else:
            self.Salt = os.urandom(16)
            self.Fernet = Fernet(self.DeriveKey())

    def SaveVault(self):
        VaultJson = {
            "Salt": base64.b64encode(self.Salt).decode(),
            "Records": []
        }

        for PasswordRecord in self.PasswordRecords:
            VaultJson["Records"].append({
                "SiteName": self.Fernet.encrypt(PasswordRecord["SiteName"].encode()).decode(),
                "Comment": self.Fernet.encrypt(PasswordRecord["Comment"].encode()).decode(),
                "Username": self.Fernet.encrypt(PasswordRecord["Username"].encode()).decode(),
                "Password": self.Fernet.encrypt(PasswordRecord["Password"].encode()).decode(),
            })

        with open(self.VaultFilePath, "w") as File:
            json.dump(VaultJson, File, indent=4)

    def AddPassword(self, PasswordRecordToAdd):
        if [PasswordRecord for PasswordRecord in self.PasswordRecords if PasswordRecord["SiteName"] == PasswordRecordToAdd["SiteName"]]:
            raise ValueError("SiteName already exists in the vault.")

        self.PasswordRecords.append(PasswordRecordToAdd)
        self.SaveVault()

    def DeletePassword(self, PasswordRecordToDelete):
        for Index, PasswordRecord in enumerate(self.PasswordRecords):
            if PasswordRecord["SiteName"] == PasswordRecordToDelete["SiteName"]:
                self.PasswordRecords.pop(Index)
                self.SaveVault()
                return

        raise ValueError("SiteName not found in the vault.")

    def EditPassword(self, PasswordRecordToEdit, PasswordRecordEdited):
        for Index, PasswordRecord in enumerate(self.PasswordRecords):
            if PasswordRecord["SiteName"] == PasswordRecordToEdit["SiteName"]:
                self.PasswordRecords[Index] = PasswordRecordEdited
                self.SaveVault()
                return

        raise ValueError("SiteName not found in the vault.")
