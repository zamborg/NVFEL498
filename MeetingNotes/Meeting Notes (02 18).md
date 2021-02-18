# Meeting Notes (02/18)

Professor Gryak's Feedback on our preliminary draft:

- Would rather have complete statements versus notes.
- Don't leave internal notes in the report and instead keep complete thoughts in the report.
- The idea is that this is a more public document and you want it to be more polished.
- For variables you would like to consider, find a way of separating the characteristics of the vehicles and considering them as classes instead of continuous variables.
- You would probably want to make your regressions 'class' based given the above consideration.
- You should put a little bit more thought into what the input/outputs would be to produce the data that you want for this system.
- When considering variables include specifics about how you are including them in the model.
- Concepts Selection:
    - One of the things that was unclear was what parts of the design your table was related to.
    - Have multiple of your kinds of tables and keep them isolated to each system/tool you are going to use for the project.
    - You could have a table for: Driver aggressiveness models, AV modeling, fuel consumption models, data inputs, dashboard tools, etc.
    - Tables that go across components are not particularly useful. (Include scales and what they mean)
    - In the system architecture piece you need to have this settled.
- Trip grouping:
    - You'll probably want to have multiple ways of grouping trips together.
    - Think about segmentation for analysis and user presentation.
    - What dials and tools would users want to use? Consider what method you are going to store information in to access it using your UI.

Discussion with Andrew:

- Q: Do you have an specifications in particular that you would like to see in the UI?
    - The ability to perform independent sensitivity analysis. EG: Nth percentile aggressive driving selection, City vs Rural driving segmentation. The ability to perform "what if" analyses.
- Q: What kind of parameters would you like to have on the dashboard?
    - Something that looks like average speed (speed of vehicle or some other factor that has to do with speed).
    - Something that looks like percentage idle time.
    - Something about the vehicle characteristics (Engine size, power to weight ratio, Displacement/weight, turbocharged, or some combination of these factors)
    - Those factors above are the things I know about, but I would like to know about things that I don't know about: Temperature, weather characteristics, etc.
- Q: Any particular UI element preferences? Dropdown boxes etc.
    - Having continuous control rather than discrete blocks for parameters that warrant this. But no particular UI element preference.
- Q: Any other metrics to prioritize other than driver aggressiveness?
    - Some way to characterize the 'driving cycle'.
    - You have a range of trips that have different average speeds as an example. Some way of describing the trip in general.
    - Think about an average vehicle, maybe thinking about the characterizations of the vehicle itself?
    - Q: What does it mean for a fleet of vehicles?
        - The ultimate metric I want to pull out is the % reduction in fuel usage.
        - Think about applying reduction to the whole fleet of cars, OR a specific vehicle.
        - Changing fleet characteristics (Ann Arbor vs New Mexico) and evaluating percentage decrease in fuel consumption.
- Q: Segmentation on vehicle type?
    - You will likely need to segment out vehicle type for analysis because sensitivity as a result of driver aggressiveness will likely be very different for hybrid EVs versus Gas cars
- Q: Would interpretable models be uniquely useful?
    - Yes, if there is something surprising in the what if analysis, it would be useful to be able to dig into the model in the background.
- Trip segmentation:
    - Two different ways of encoding trips:
        - Key in → Key out (looks like what the dataset reflects)
        - Microtrips or trip segments:
            - Time you start at one stoplight till you start again at the next stoplight.
            - Essentially a continuous movement as a single trip
            - City has multiple trips (start/stop/start/stop)
            - Highway driving might be entirely one trip.
    - Might be useful to look at an entire trip and consider the different driving styles around the trip.
    - Could think about standard deviation of speed across a trip for segmentation into sections.