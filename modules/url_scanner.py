import base64
import asyncio
import aiohttp

from config import VIRUSTOTAL_API_KEY


# ==================================
# VIRUSTOTAL CONFIG
# ==================================


VT_BASE_URL = "https://www.virustotal.com/api/v3"




class VirusTotalURLScanner:


    def __init__(self):

        self.headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }



    # ==============================
    # ENCODE URL (VT URL ID FORMAT)
    # ==============================


    def encode_url(
        self,
        url
    ):

        return (
            base64
            .urlsafe_b64encode(url.encode())
            .decode()
            .strip("=")
        )



    # ==============================
    # SUBMIT URL FOR ANALYSIS
    # ==============================


    async def submit_url(
        self,
        url
    ):

        if not VIRUSTOTAL_API_KEY:

            return {
                "success": False,
                "error": "Missing API Key"
            }


        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f"{VT_BASE_URL}/urls",
                    headers=self.headers,
                    data={"url": url}
                ) as response:

                    data = await response.json()

                    if response.status not in [200, 201]:

                        return {
                            "success": False,
                            "error": data
                        }

                    return {
                        "success": True,
                        "analysis_id": data["data"]["id"]
                    }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }



    # ==============================
    # GET ANALYSIS STATUS
    # ==============================


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



    # ==============================
    # WAIT UNTIL SCAN COMPLETED
    # ==============================


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



    # ==============================
    # CALCULATE RISK LEVEL
    # ==============================


    def calculate_risk(
        self,
        detected
    ):

        if detected == 0:

            return {
                "level": "safe",
                "key": "safe"
            }

        elif detected <= 2:

            return {
                "level": "low",
                "key": "suspicious_low"
            }

        elif detected <= 5:

            return {
                "level": "medium",
                "key": "suspicious"
            }

        elif detected <= 15:

            return {
                "level": "high",
                "key": "dangerous"
            }

        else:

            return {
                "level": "critical",
                "key": "critical"
            }



    # ==============================
    # PARSE RESULT
    # ==============================


    def parse_result(
        self,
        result,
        url
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

        total = sum(stats.values()) if stats else 0

        threats = []

        # VirusTotal returns "results" as a dict: {engine_name: {...}}
        for engine_result in attr.get("results", {}).values():

            if engine_result.get("category") == "malicious":

                if engine_result.get("result"):

                    threats.append(
                        engine_result["result"]
                    )

        risk = self.calculate_risk(
            detected
        )

        return {

            "url": url,

            "detected": detected,

            "total": total,

            "risk": risk["level"],

            "message_key": risk["key"],

            "threats": list(set(threats))[:3],

            "report_url":
            f"https://www.virustotal.com/gui/url/{self.encode_url(url)}"

        }



    # ==============================
    # SCAN URL (FULL FLOW)
    # ==============================


    async def scan(
        self,
        url
    ):

        submit = await self.submit_url(
            url
        )

        if not submit["success"]:

            return submit

        result = await self.wait_scan(
            submit["analysis_id"]
        )

        if not result:

            return {
                "success": False,
                "error": "Timeout"
            }

        data = self.parse_result(
            result,
            url
        )

        data["success"] = True

        return data




# ==================================
# SHORTCUT FUNCTION
# ==================================


async def scan_url(
    url
):

    scanner = VirusTotalURLScanner()

    return await scanner.scan(
        url
    )
