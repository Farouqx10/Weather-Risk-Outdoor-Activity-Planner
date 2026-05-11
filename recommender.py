class RecommendationEngine:

    def get_best_time(self, forecast):
        temp = forecast.temperature
        rain = forecast.rain

        if temp is not None and temp > 32:
            return "Early morning or late evening"
        if rain and rain > 5:
            return "Wait until the rain stops"
        if rain and rain > 0:
            return "Midday when rain is lighter"
        return "Anytime is fine"

    def packing_list(self, activity):
        base_items = ["Water bottle", "Phone"]
        activity_items = {"Football": ["Boots", "Jersey"], 
        "Jogging": ["Running shoes"], "Farming": ["Gloves", "Boots"], 
        "Picnic": ["Mat", "Snacks"], "Travel": ["Backpack", "Documents"], 
        "Outdoor Event": ["Comfy clothes"]
        }
        return base_items + activity_items.get(activity, [])

    def safety_tips(self, forecast):
        tips = []

        if forecast.temperature and forecast.temperature > 35:
            tips.append("Avoid prolonged exposure to heat")
        if forecast.rain and forecast.rain > 0:
            tips.append("Carry an umbrella or a raincoat")
        if forecast.windspeed > 30:
            tips.append("Be cautious of strong winds")
        if not tips:
            tips.append("Weather conditions are favorable")
        return tips