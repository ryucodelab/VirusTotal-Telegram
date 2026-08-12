import os
import asyncio
import aiohttp

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


VT_API_KEY = os.getenv(
    "VIRUSTOTAL_API_KEY"
)


VT_BASE_URL = (
    "https://www.virustotal.com/api/v3"
)



class VirusTotalScanner:


    def __init__(self):

        self.headers = {
            "x-apikey": VT_API_KEY
        }



    async def upload_file(
        self,
        file_path
    ):

        if not VT_API_KEY:

            return {
                "success": False,
                "error": "Missing API Key"
            }


        try:

            async with aiohttp.ClientSession() as session:

                with open(
                    file_path,
                    "rb"
                ) as file:


                    form = aiohttp.FormData()


                    form.add_field(
                        "file",
                        file,
                        filename=Path(file_path).name
                    )


                    async with session.post(
                        f"{VT_BASE_URL}/files",
                        headers=self.headers,
                        data=form
                    ) as response:


                        data = await response.json()


                        if response.status not in [200,201]:

                            return {
                                "success":False,
                                "error":data
                            }


                        return {

                            "success":True,

                            "analysis_id":
                            data["data"]["id"]

                        }


        except Exception as e:


            return {

                "success":False,

                "error":str(e)

            }





    async def get_analysis(
        self,
        analysis_id
    ):


        async with aiohttp.ClientSession() as session:


            async with session.get(
                f"{VT_BASE_URL}/analyses/{analysis_id}",
                headers=self.headers
            ) as response:


                return await response.json()







    async def wait_scan(
        self,
        analysis_id
    ):


        for _ in range(36):


            result = await self.get_analysis(
                analysis_id
            )


            status = (
                result
                .get("data", {})
                .get("attributes", {})
                .get("status")
            )


            if status == "completed":

                return result



            await asyncio.sleep(5)



        return None







    def calculate_risk(
        self,
        detected
    ):


        if detected == 0:

            return {
                "level":"safe",
                "key":"safe"
            }


        elif detected <= 2:

            return {
                "level":"low",
                "key":"suspicious_low"
            }


        elif detected <= 5:

            return {
                "level":"medium",
                "key":"suspicious"
            }


        elif detected <= 15:

            return {
                "level":"high",
                "key":"dangerous"
            }


        else:

            return {
                "level":"critical",
                "key":"critical"
            }






    def parse_result(
        self,
        result,
        file_path
    ):


        attr = (
            result
            .get("data", {})
            .get("attributes", {})
        )


        stats = attr.get(
            "stats",
            {}
        )


        detected = stats.get(
            "malicious",
            0
        )


        total = sum(
            stats.values()
        )



        threats=[]


        for engine in attr.get(
            "results",
            []
        ):


            if engine.get(
                "category"
            ) == "malicious":


                if engine.get(
                    "result"
                ):

                    threats.append(
                        engine["result"]
                    )




        risk = self.calculate_risk(
            detected
        )



        return {


            "file_name":
            Path(file_path).name,


            "file_type":
            attr.get(
                "type_description",
                "Unknown"
            ),


            "sha256":
            attr.get(
                "sha256",
                "-"
            ),


            "detected":
            detected,


            "total":
            total,


            "risk":
            risk["level"],


            "message_key":
            risk["key"],


            "threats":
            list(
                set(threats)
            )[:3],


            "report_url":
            (
                "https://www.virustotal.com/gui/file/"
                +
                attr.get(
                    "sha256",
                    ""
                )
            )

        }






    async def scan(
        self,
        file_path
    ):


        upload = await self.upload_file(
            file_path
        )


        if not upload["success"]:

            return upload



        result = await self.wait_scan(
            upload["analysis_id"]
        )


        if not result:

            return {

                "success":False,

                "error":
                "Timeout"

            }




        data = self.parse_result(
            result,
            file_path
        )


        data["success"]=True


        return data





async def scan_file(
    file_path
):

    scanner = VirusTotalScanner()

    return await scanner.scan(
        file_path
    )