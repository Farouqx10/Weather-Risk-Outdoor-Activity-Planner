from google import genai

class ActivityRiskAnalyzer:

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def analyze(self, activity, forecast):
        temperature = forecast.temperature
        windspeed = forecast.windspeed
        rain = forecast.rain

        if rain and rain > 5:
            return "Avoid"
        if temperature is  not None and temperature > 35:
            return "Risky"
        if windspeed is not None and windspeed > 30:
            return "Manageable"
        if rain and rain > 0:
            return "Manageable"
        return "Safe"
            
    def ai_analysis(self, activity, forecast):
        prompt = f""" You are a weather safety assistant.
        Activity: {activity}
        Temperature: {forecast.temperature}°C
        Wind Speed: {forecast.windspeed}km/h
        Rain: {forecast.rain}mm

        1. Classify the risk (Safe, Manageable, Risky, Avoid)
        2. Explain why
        3. Suggest best time of day
        4. Give safety advice
        5. Provide a packing checklist

        Keep it short and clear.
        """

        try:
            response = self.client.models.generate_content(model="models/gemini-1.5-flash",contents=prompt)
            try:
                return response.text
            except:
                return str(response)
        except Exception:
            risk = self.analyze(activity, forecast)

            if risk == "Safe":
                return f"""
                The weather looks favourable for {activity}.

                Best Time:
                Morning or evening.

                Advice:
                Stay hydrated and wear comfortable clothes.
                    
                Packing:
                Water bottle, light clothes, sunscreen.
                """
            elif risk == "Manageable":
                return f"""
                The activity is manageable but requires caution.

                Best Time:
                Early Morning

                Advice:
                Monitor weather changes and avoid prolonged exposure.

                Packing:
                Umbrella, water bottle, comfortable shoes.
                """
            elif risk == "Risky":
                return f"""
                Weather conditions may make {activity} uncomortable or risky.
                
                Best Time:
                Very early in the morning or postpone if possible.

                Advice:
                Limit outdoor exposure and stay alert.

                Packing:
                Protective clothing, water, weather protection gear.
                """
            else:
                return f"""
                It is recommended to avoid {activity} due to poor weather conditions.

                Advice:
                Consider postponing the activity until the conditions improve.
                
                Packing:
                Emergency essentials and rain protection if outing is necessary.
                """