"""Bilingual (English / Hinglish) lesson content, quiz and safe home activities.

Language keys: "en" = English, "hi" = Hinglish (Hindi written in English letters).
"""
from __future__ import annotations

# ----------------------------------------------------------------------------- human body
BODY_PARTS = [
    dict(key="brain", system="Nervous system", en_name="Brain", hi_name="Dimaag (Brain)",
         en="The brain is your body's control room. It helps you think, remember, move and feel. "
            "It sends messages through nerves to every part of you.",
         hi="Brain (dimaag) hamare sharir ka control room hai. Yeh sochne, yaad rakhne, chalne aur mehsoos karne "
            "mein help karta hai. Yeh nerves ke through poore sharir ko messages bhejta hai.",
         fact_en="Your brain uses about 20% of your body's energy!",
         fact_hi="Brain sharir ki lagbhag 20% energy use karta hai!",
         keywords=["brain", "dimaag", "dimag", "mind", "nervous", "sochna"]),
    dict(key="lungs", system="Respiratory system", en_name="Lungs", hi_name="Fefde (Lungs)",
         en="Lungs help you breathe. When you breathe in, they take oxygen from the air. When you breathe out, "
            "they send out carbon dioxide.",
         hi="Fefde (lungs) hamein saans lene mein help karte hain. Saans andar lete waqt yeh hawa se oxygen lete "
            "hain aur saans bahar chhodte waqt carbon dioxide bahar nikalte hain.",
         fact_en="You breathe about 20,000 times every day!",
         fact_hi="Hum roz lagbhag 20,000 baar saans lete hain!",
         keywords=["lungs", "lung", "fefde", "phephde", "fefda", "breathe", "breathing", "saans", "respiratory"]),
    dict(key="heart", system="Circulatory system", en_name="Heart", hi_name="Dil (Heart)",
         en="The heart is a strong muscle that pumps blood around your body. Blood carries oxygen and food to "
            "every part of you.",
         hi="Dil (heart) ek majboot muscle hai jo poore sharir mein khoon pump karta hai. Khoon har hisse tak "
            "oxygen aur poshan pahunchata hai.",
         fact_en="Your heart is about the size of your fist and beats around 100,000 times a day!",
         fact_hi="Tumhara dil lagbhag tumhari mutthi jitna bada hota hai aur din mein lagbhag 1,00,000 baar "
                 "dhadakta hai!",
         keywords=["heart", "dil", "dhadkan", "blood", "khoon", "circulatory", "pump"]),
    dict(key="stomach", system="Digestive system", en_name="Stomach", hi_name="Pet / Stomach (Mehda)",
         en="Food goes down the food pipe into the stomach. The stomach churns the food and mixes it with acid "
            "and juices to break it into tiny pieces.",
         hi="Khana food pipe se hokar stomach (mehda) mein jaata hai. Stomach khane ko ghumata hai aur acid aur "
            "juices mila kar chhote-chhote tukdon mein tod deta hai.",
         fact_en="Your stomach has a special layer so its own acid doesn't hurt it!",
         fact_hi="Stomach ki ek khaas layer hoti hai jisse uska apna acid use nuksaan nahi pahunchata!",
         keywords=["stomach", "pet", "mehda", "digest", "digestion", "digestive", "khana", "food"]),
    dict(key="liver", system="Digestive system", en_name="Liver", hi_name="Jigar (Liver)",
         en="The liver cleans your blood, helps digest fat and stores energy. It is the biggest organ inside "
            "your body.",
         hi="Jigar (liver) khoon ko saaf karta hai, fat pachane mein help karta hai aur energy store karta hai. "
            "Yeh sharir ke andar ka sabse bada organ hai.",
         fact_en="The liver can grow back a part of itself after an injury!",
         fact_hi="Chot lagne ke baad liver apna kuch hissa dobara ugaa sakta hai!",
         keywords=["liver", "jigar", "bile"]),
    dict(key="kidneys", system="Urinary system", en_name="Kidneys", hi_name="Gurde (Kidneys)",
         en="You have two bean-shaped kidneys. They filter your blood, remove waste and extra water, and make "
            "urine.",
         hi="Humare do rajma jaise aakar ke gurde (kidneys) hote hain. Yeh khoon ko filter karte hain, kachra aur "
            "extra paani nikalte hain aur urine banate hain.",
         fact_en="Your kidneys filter all your blood about 40 times a day!",
         fact_hi="Gurde din mein lagbhag 40 baar poora khoon filter karte hain!",
         keywords=["kidney", "kidneys", "gurde", "gurda", "urine", "filter"]),
    dict(key="intestines", system="Digestive system", en_name="Intestines", hi_name="Aant (Intestines)",
         en="After the stomach, food moves into the small and large intestines. The small intestine takes the "
            "good nutrients into your blood and the large intestine takes back water.",
         hi="Stomach ke baad khana chhoti aur badi aant (intestines) mein jaata hai. Chhoti aant poshan ko khoon "
            "mein pahunchati hai aur badi aant paani wapas leti hai.",
         fact_en="Your small intestine is about 6 metres long, longer than a car!",
         fact_hi="Chhoti aant lagbhag 6 metre lambi hoti hai, ek car se bhi lambi!",
         keywords=["intestine", "intestines", "aant", "aanten", "bowel", "nutrients"]),
    dict(key="bones", system="Skeletal system", en_name="Bones (Skeleton)", hi_name="Haddiyan (Bones)",
         en="Bones give your body shape, protect organs (ribs protect the heart and lungs, the skull protects "
            "the brain) and help you move together with muscles.",
         hi="Haddiyan (bones) sharir ko shape deti hain, organs ko bachati hain (ribs dil aur fefdon ko, skull "
            "dimaag ko) aur muscles ke saath milkar chalne-phirne mein help karti hain.",
         fact_en="An adult has 206 bones, but a baby is born with about 300!",
         fact_hi="Bade insaan mein 206 haddiyan hoti hain, lekin ek baby lagbhag 300 haddiyon ke saath paida "
                 "hota hai!",
         keywords=["bone", "bones", "haddi", "haddiyan", "skeleton", "skeletal", "skull", "ribs"]),
]
BODY_BY_KEY = {b["key"]: b for b in BODY_PARTS}

# ----------------------------------------------------------------------------- physics
PHYSICS = {
    "projectile": dict(
        title_en="Projectile motion (throwing a ball)", title_hi="Projectile motion (gend phenkna)",
        en="When you throw a ball, gravity pulls it down while it moves forward, so it flies in a curve called a "
           "parabola. On Earth, a throw at about 45 degrees goes the farthest.",
        hi="Jab tum gend phenkte ho, gravity use neeche kheenchti hai aur woh aage badhti hai, isliye woh ek curve "
           "(parabola) mein udti hai. Earth par lagbhag 45 degree ke angle par phenkne se gend sabse door jaati hai.",
        formula="Range = v² × sin(2θ) / g",
        activity_en="Throw a soft ball outside at low, medium and high angles (with an adult). Which angle goes "
                    "farthest? Measure the distance with steps!",
        activity_hi="Bahar kisi bade ke saath ek soft ball alag-alag angle par phenko. Kaun sa angle sabse door "
                    "jaata hai? Kadmon se doori naapo!",
        keywords=["projectile", "parabola", "trajectory", "gend", "ball", "throw", "phenkna", "angle", "gravity",
                  "gurutvakarshan"]),
    "pendulum": dict(
        title_en="Pendulum (swinging)", title_hi="Pendulum (jhoolna)",
        en="A pendulum swings back and forth. A longer string makes it swing more slowly. The time for one full "
           "swing is called the time period, and the weight of the bob doesn't change it.",
        hi="Pendulum aage-peeche jhoolta hai. Dhaga lamba ho toh woh dheere jhoolta hai. Ek poore jhoole ke time ko "
           "time period kehte hain, aur bob ka wazan isse nahi badalta.",
        formula="T = 2π × √(L / g)",
        activity_en="Tie a small weight to a string and swing it. Count swings in 10 seconds with a short and a "
                    "long string. Which swings faster?",
        activity_hi="Ek chhota wazan dhaage se baandh kar jhulao. 10 second mein jhoole ginno, pehle chhote aur "
                    "phir lambe dhaage ke saath. Kaun tez jhoolta hai?",
        keywords=["pendulum", "swing", "jhoola", "jhoolna", "oscillation", "time period", "clock"]),
    "ohm": dict(
        title_en="Ohm's law (electric circuit)", title_hi="Ohm's law (bijli ka circuit)",
        en="In a circuit, voltage (V) pushes current (I) through a resistance (R). More voltage means more "
           "current; more resistance means less current. That is Ohm's law: V = I × R.",
        hi="Circuit mein voltage (V) current (I) ko resistance (R) ke through dhakelta hai. Zyada voltage matlab "
           "zyada current; zyada resistance matlab kam current. Yahi Ohm's law hai: V = I × R.",
        formula="V = I × R",
        activity_en="Safe version: with a torch (flashlight) and a 1.5 V battery, notice how a weaker battery gives "
                    "a dimmer bulb. Never touch mains sockets or wires!",
        activity_hi="Safe tareeka: torch aur 1.5 V ki battery se dekho ki kamzor battery se bulb dim jalta hai. "
                    "Ghar ke plug-socket ya wires ko kabhi mat chhuo!",
        keywords=["ohm", "ohms", "ohms law", "ohm's law", "ohm law", "circuit", "current", "voltage", "resistance", "bijli", "electricity",
                  "electric", "battery", "bulb"]),
    "refraction": dict(
        title_en="Refraction (bending of light)", title_hi="Refraction (roshni ka mudna)",
        en="Light bends when it goes from one material into another, like from air into water. That's why a "
           "straw in a glass of water looks bent. This bending is called refraction.",
        hi="Roshni jab ek padarth se doosre mein jaati hai, jaise hawa se paani mein, toh woh mud jaati hai. "
           "Isliye paani ke glass mein straw tedhi dikhti hai. Is mudne ko refraction kehte hain.",
        formula="n₁ × sin(θ₁) = n₂ × sin(θ₂)",
        activity_en="Put a pencil in a clear glass of water and look from the side. Why does it look broken?",
        activity_hi="Ek saaf glass paani mein pencil rakho aur side se dekho. Woh tuti hui kyun dikhti hai?",
        keywords=["refraction", "light", "roshni", "bend", "mudna", "snell", "lens", "reflection", "prism"]),
    "force": dict(
        title_en="Force & Newton's Laws of Motion (F = m × a)", title_hi="Force aur Newton ke Niyam (F = m × a)",
        en="A force is simply a push or a pull! Sir Isaac Newton gave 3 Laws of Motion:\n\n"
           "1. 1st Law (Inertia): An object stays at rest or moves at a constant speed unless a force acts on it.\n"
           "2. 2nd Law (F = m × a): Force = Mass × Acceleration. A heavier object needs more force to speed up!\n"
           "3. 3rd Law (Action & Reaction): For every action, there is an equal and opposite reaction.\n\n"
           "📐 Formula: Force = Mass × Acceleration (F = m × a). Unit: Newton (N).",
        hi="Force (bal) kisi cheez ko dhakka dena (push) ya kheenchna (pull) hota hai! Newton ke 3 Niyam:\n\n"
           "1. 1st Law (Inertia): Har cheez apni jagah rehti hai jab tak uspar force na lage.\n"
           "2. 2nd Law (F = m × a): Force = Mass × Acceleration. Bhaari cheez ko chalane ke liye zyada force chahiye!\n"
           "3. 3rd Law (Action & Reaction): Har action ka ek barabar aur ulta reaction hota hai.\n\n"
           "📐 Formula: F = m × a. Unit: Newton (N).",
        formula="F = m × a",
        activity_en="Push a light ball and a heavy book with the same push. The light ball accelerates much faster because of Newton's 2nd Law (F = m × a)!",
        activity_hi="Ek halki ball aur ek bhaari kitaab ko dhakka do. Halki ball tez bhaagti hai kyunki F = m × a!",
        keywords=["force", "bal", "push", "pull", "motion", "gati", "newton", "newtons", "newtons law", "newtons laws",
                  "newton's", "newtons 2nd law", "newton 2nd law", "second law", "2nd law", "newtons second law",
                  "newtons 1st law", "first law", "1st law", "inertia", "newtons 3rd law", "third law", "3rd law",
                  "action and reaction", "acceleration", "mass", "f=ma", "f = ma", "dhakka", "kheenchna", "speed",
                  "friction", "laws of motion"]),
    "sky": dict(
        title_en="Why is the sky blue? (Rayleigh scattering)", title_hi="Aasman neela kyun hai? (Rayleigh scattering)",
        en="Sunlight looks white, but it holds all rainbow colors! Blue light travels in short, small waves and "
           "gets scattered in all directions by air molecules in Earth's atmosphere. That is why the sky appears bright blue!",
        hi="Suraj ki roshni mein rainbow ke 7 rang hote hain! Blue light chhote waves mein chalti hai aur hawa ke "
           "molecules se takra kar charon taraf phail (scatter) jaati hai. Isliye din mein aasman neela dikhta hai!",
        formula="Scattering ∝ 1 / λ⁴",
        activity_en="In a dark room, shine a torch through a clear glass of water with a few drops of milk. Look at the bluish glow from the side!",
        activity_hi="Andhere kamre mein paani ke glass mein 2 boond doodh milao aur torch ki roshni daalo. Side se halki neeli glow dikhegi!",
        keywords=["sky", "blue", "blue sky", "aasman", "neela", "scattering", "rayleigh", "sunlight", "atmosphere",
                  "roshni", "rainbow", "waves"]),
    "gravity": dict(
        title_en="Gravity (Why things fall down)", title_hi="Gravity (Cheezein neeche kyun girti hain)",
        en="Gravity is an invisible pulling force between all masses in the universe. Earth's gravity pulls everything "
           "towards its centre, keeping our feet on the ground and giving objects weight (w = m × g).",
        hi="Gravity ek aisi adrishya force hai jo har cheez ko apni taraf kheenchti hai. Dharti ki gravity sabhi "
           "cheezon ko center ki taraf kheenchti hai, jisse hum zameen par khade rehte hain (w = m × g).",
        formula="w = m × g  •  g ≈ 9.8 m/s²",
        activity_en="Drop a flat paper sheet and a crumpled paper ball together from shoulder height. Why does the crumpled ball land first? (Air resistance!)",
        activity_hi="Ek seedha kagaz aur ek mod kar banayi kagaz ki ball ek saath giraao. Kaun pehle girti hai aur kyun?",
        keywords=["gravity", "gurutvakarshan", "fall", "girna", "weight", "earth", "mass", "newton", "orbit", "pull"]),
    "friction": dict(
        title_en="Friction (Grip, Heat & Stopping)", title_hi="Friction / Gharshan (Rukna aur Garmi)",
        en="Friction is the resistive force that opposes motion when two surfaces touch each other. "
           "It creates heat, helps you walk without slipping, and lets car brakes stop the wheels safely.",
        hi="Friction (gharshan) do satah ke chhoone par gati ko rokne wali force hai. Yeh garmi paida karti hai, "
           "humein bina phisle chalne mein help karti hai aur gaadiyon ke break lagane mein zaroori hoti hai.",
        formula="f = μ × N",
        activity_en="Rub your palms together quickly for 10 seconds. Feel them get warm? That is friction creating heat!",
        activity_hi="Apni dono hatheliyon ko tezi se 10 second ragdo. Garam lagti hain? Yeh friction ki wajah se heat banti hai!",
        keywords=["friction", "gharshan", "grip", "slip", "sliding", "rolling", "heat", "brakes", "rough", "smooth"]),
    "push_pull": dict(
        title_en="Push & Pull Forces (How Things Move)", title_hi="Push aur Pull Force (Cheezein Kaise Chalti Hain)",
        en="Every movement starts with a push or a pull! Pushing moves things away from you (like kicking a ball or rolling a toy car). Pulling brings things towards you (like pulling a wagon or a rope)!",
        hi="Har gati push ya pull se shuru hoti hai! Dhakka dene (push) se cheez door jaati hai jaise ball ko kick karna. Kheenchna (pull) cheez ko paas lata hai jaise wagon kheenchna!",
        formula="Push (Away) • Pull (Towards)",
        activity_en="Roll a toy car on the floor. First push it gently, then pull it back with a string!",
        activity_hi="Floor par toy car ko chalao. Pehle dhakka do, phir dhaage se apni taraf kheencho!",
        keywords=["push", "pull", "force", "dhakka", "kheenchna", "toy car", "move", "movement"]),
}

# ----------------------------------------------------------------------------- chemistry
ELEMENTS = [  # (Z, symbol, name, neutrons)
    (1, "H", "Hydrogen", 0), (2, "He", "Helium", 2), (3, "Li", "Lithium", 4), (4, "Be", "Beryllium", 5),
    (5, "B", "Boron", 6), (6, "C", "Carbon", 6), (7, "N", "Nitrogen", 7), (8, "O", "Oxygen", 8),
    (9, "F", "Fluorine", 10), (10, "Ne", "Neon", 10), (11, "Na", "Sodium", 12), (12, "Mg", "Magnesium", 12),
    (13, "Al", "Aluminium", 14), (14, "Si", "Silicon", 14), (15, "P", "Phosphorus", 16), (16, "S", "Sulphur", 16),
    (17, "Cl", "Chlorine", 18), (18, "Ar", "Argon", 22), (19, "K", "Potassium", 20), (20, "Ca", "Calcium", 20),
]
ELEMENT_BY_Z = {e[0]: e for e in ELEMENTS}

ELEMENT_USE = {
    1: ("the lightest element and part of water", "sabse halka element hai aur paani ka hissa hai"),
    2: ("used to fill party balloons that float", "float karne wale party balloons mein bharti hai"),
    6: ("found in all living things, pencil lead and diamonds", "sabhi jeevon, pencil ki lead aur heere mein hota hai"),
    7: ("makes up most of the air we breathe", "hamari hawa ka sabse bada hissa hai"),
    8: ("the gas we need to breathe to stay alive", "woh gas jo zinda rehne ke liye saans mein chahiye"),
    10: ("glows red-orange in shop signs", "dukaan ke signboards mein laal-narangi chamakti hai"),
    11: ("part of common salt", "namak ka hissa hai"),
    17: ("part of salt and helps make drinking water safe", "namak ka hissa hai aur paani ko surakshit banata hai"),
    20: ("makes our bones and teeth strong", "hamari haddiyon aur daanton ko mazboot banata hai"),
}

MOLECULES = {
    "H2O": dict(name_en="Water", name_hi="Paani (Water)", formula="H₂O",
                atoms=[("O", 0, 0.35), ("H", -0.85, -0.3), ("H", 0.85, -0.3)], bonds=[(0, 1, 1), (0, 2, 1)],
                en="Water has 2 hydrogen atoms and 1 oxygen atom joined together. Life on Earth needs it!",
                hi="Paani mein 2 hydrogen aur 1 oxygen atom jude hote hain. Dharti par jeevan ko iski zarurat hai!"),
    "CO2": dict(name_en="Carbon dioxide", name_hi="Carbon dioxide", formula="CO₂",
                atoms=[("O", -1.3, 0), ("C", 0, 0), ("O", 1.3, 0)], bonds=[(0, 1, 2), (1, 2, 2)],
                en="Carbon dioxide has 1 carbon and 2 oxygen atoms. We breathe it out and plants use it to make food.",
                hi="Carbon dioxide mein 1 carbon aur 2 oxygen atom hote hain. Hum ise saans mein bahar chhodte hain "
                   "aur paudhe ise khana banane mein use karte hain."),
    "CH4": dict(name_en="Methane", name_hi="Methane", formula="CH₄",
                atoms=[("C", 0, 0), ("H", -0.9, 0.9), ("H", 0.9, 0.9), ("H", -0.9, -0.9), ("H", 0.9, -0.9)],
                bonds=[(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
                en="Methane has 1 carbon and 4 hydrogen atoms. It is the main gas in natural gas used for cooking.",
                hi="Methane mein 1 carbon aur 4 hydrogen atom hote hain. Cooking mein use hone wali natural gas ka "
                   "mukhya hissa yahi hai."),
    "O2": dict(name_en="Oxygen gas", name_hi="Oxygen gas", formula="O₂",
               atoms=[("O", -0.65, 0), ("O", 0.65, 0)], bonds=[(0, 1, 2)],
               en="Two oxygen atoms joined by a double bond make the oxygen we breathe.",
               hi="Do oxygen atom double bond se jud kar woh oxygen banate hain jo hum saans mein lete hain."),
    "NH3": dict(name_en="Ammonia", name_hi="Ammonia", formula="NH₃",
                atoms=[("N", 0, 0.45), ("H", -0.95, -0.3), ("H", 0.95, -0.3), ("H", 0, -1.0)],
                bonds=[(0, 1, 1), (0, 2, 1), (0, 3, 1)],
                en="Ammonia has 1 nitrogen and 3 hydrogen atoms. It has a sharp smell and is used in fertilisers.",
                hi="Ammonia mein 1 nitrogen aur 3 hydrogen atom hote hain. Isse tez smell aati hai aur yeh khaad "
                   "(fertiliser) banane mein use hota hai."),
    "HCl": dict(name_en="Hydrogen chloride", name_hi="Hydrogen chloride", formula="HCl",
                atoms=[("H", -0.7, 0), ("Cl", 0.7, 0)], bonds=[(0, 1, 1)],
                en="One hydrogen and one chlorine atom. Dissolved in water it becomes hydrochloric acid, also found in "
                   "our stomach in a weak form.",
                hi="Ek hydrogen aur ek chlorine atom. Paani mein ghulne par hydrochloric acid banta hai, jo kamzor "
                   "roop mein hamare pet mein bhi hota hai."),
}

STATES = {
    "solid": dict(en_name="Solid", hi_name="Thos (Solid)",
                  en="In a solid, particles are packed tightly and only vibrate in place. That's why solids keep "
                     "their shape, like ice.",
                  hi="Solid mein particles ek-doosre se kase hue hote hain aur sirf apni jagah par kaanpte hain. "
                     "Isliye solid apna shape banaye rakhta hai, jaise barf."),
    "liquid": dict(en_name="Liquid", hi_name="Taral (Liquid)",
                   en="In a liquid, particles are close but can slide past each other. That's why liquids flow and "
                      "take the shape of their container.",
                   hi="Liquid mein particles paas-paas hote hain lekin ek-doosre ke upar se phisal sakte hain. "
                      "Isliye liquid behta hai aur bartan ka shape le leta hai."),
    "gas": dict(en_name="Gas", hi_name="Gas",
                en="In a gas, particles are far apart and zoom around quickly, filling the whole space available.",
                hi="Gas mein particles door-door hote hain aur tezi se idhar-udhar bhaagte hain, aur poori jagah "
                   "bhar dete hain."),
}

PH_SUBSTANCES = {  # key: (en, hi, pH)
    "stomach_acid": ("Stomach acid", "Pet ka acid", 1.5),
    "lemon": ("Lemon juice", "Nimbu ka ras", 2.0),
    "vinegar": ("Vinegar", "Sirka", 3.0),
    "tomato": ("Tomato", "Tamatar", 4.3),
    "coffee": ("Black coffee", "Black coffee", 5.0),
    "milk": ("Milk", "Doodh", 6.5),
    "water": ("Pure water", "Saaf paani", 7.0),
    "blood": ("Human blood", "Insaani khoon", 7.4),
    "baking_soda": ("Baking soda solution", "Meetha soda ka ghol", 9.0),
    "soap": ("Soap", "Sabun", 10.0),
    "bleach": ("Bleach (never touch!)", "Bleach (kabhi mat chhuo!)", 13.0),
}

CHEM_TEXT = {
    "atom": dict(
        title_en="Atoms", title_hi="Atoms (parmanu)",
        en="Everything is made of tiny atoms. An atom has a centre called the nucleus (protons and neutrons) and "
           "electrons moving around it in shells.",
        hi="Har cheez chhote-chhote atoms (parmanu) se bani hai. Atom ke beech mein nucleus hota hai (protons aur "
           "neutrons) aur uske charon taraf shells mein electrons ghumte hain.",
        keywords=["atom", "atoms", "parmanu", "proton", "neutron", "electron", "nucleus", "shell", "bohr"]),
    "molecule": dict(
        title_en="Molecules", title_hi="Molecules (anu)",
        en="When atoms join together they make a molecule, like two hydrogens and one oxygen making water.",
        hi="Jab atoms jud jaate hain toh molecule (anu) banta hai, jaise do hydrogen aur ek oxygen milkar paani "
           "banate hain.",
        keywords=["molecule", "molecules", "anu", "bond", "compound", "formula", "water", "paani", "pani"]),
    "states": dict(
        title_en="States of matter", title_hi="Padarth ki avasthayein (States of matter)",
        en="Matter mostly exists as solid, liquid or gas. Heating makes particles move faster, so ice can melt "
           "into water and water can turn into steam.",
        hi="Padarth mostly solid, liquid ya gas roop mein hota hai. Garmi se particles tez chalte hain, isliye "
           "barf pighal kar paani aur paani bhaap ban sakta hai.",
        keywords=["solid", "liquid", "gas", "state", "states", "matter", "melt", "pighalna", "bhaap", "steam",
                  "ice", "barf", "evaporation", "boiling"]),
    "ph": dict(
        title_en="Acids and bases (pH)", title_hi="Acid aur base (pH)",
        en="The pH scale goes from 0 to 14. Below 7 is acid (like lemon), 7 is neutral (pure water) and above 7 "
           "is a base (like soap).",
        hi="pH scale 0 se 14 tak hota hai. 7 se neeche acid (jaise nimbu), 7 neutral (saaf paani) aur 7 se upar "
           "base (jaise sabun) hota hai.",
        keywords=["ph", "acid", "base", "acidic", "alkaline", "neutral", "nimbu", "lemon", "indicator"]),
    "metals": dict(
        title_en="Metals & Non-Metals in Daily Life", title_hi="Metals aur Non-Metals (Dhaatu aur Adhaatu)",
        en="Metals and Non-Metals are essential materials in our daily life!\n\n"
           "🥇 **Importance of Metals:**\n"
           "• **Iron (Fe):** High strength for building bridges, trains, houses, and tools.\n"
           "• **Copper (Cu) & Aluminium (Al):** Outstanding conductors of electricity & heat, used in electrical wiring and cooking pots.\n"
           "• **Gold (Au) & Silver (Ag):** Highly lustrous and corrosion-resistant, used for jewelry and premium electronics.\n\n"
           "🧪 **Importance of Non-Metals:**\n"
           "• **Oxygen (O₂):** Vital for breathing (respiration) of humans, animals, and plants.\n"
           "• **Nitrogen (N) & Phosphorus (P):** Essential in fertilizers for rich crop yields.\n"
           "• **Carbon (C):** Present in all living beings, food, diamonds, and pencil graphite.\n"
           "• **Chlorine (Cl):** Water purifier that destroys germs to make water safe to drink.\n"
           "• **Iodine (I):** Used as an antiseptic tincture on cuts and wounds.\n\n"
           "💡 **Key Properties:** Metals are malleable (beaten into sheets), ductile (drawn into wires), and sonorous. Non-metals are brittle insulators!",
        hi="Metals (Dhaatu) aur Non-Metals (Adhaatu) hamare rozmarra ke jeevan mein behad zaroori hain!\n\n"
           "🥇 **Metals ka Mahatva (Daily Life Uses):**\n"
           "• **Loha (Iron):** Mazbooti ke kaaran pul, makaan, train aur gaadiyan banane mein use hota hai.\n"
           "• **Taamba (Copper) aur Aluminium:** Bijli ki taarein aur khana banane ke bartan mein kaam aate hain.\n"
           "• **Sona (Gold) aur Chandi (Silver):** Gehne banane mein use hote hain kyunki inmein chamak hoti hai aur zang nahi lagta.\n\n"
           "🧪 **Non-Metals ka Mahatva (Daily Life Uses):**\n"
           "• **Oxygen:** Sabhi jeevon ke saans lene aur zinda rehne ke liye sabse zaroori gas hai!\n"
           "• **Nitrogen aur Phosphorus:** Kheti mein khaad (fertilizers) banane mein kaam aate hain.\n"
           "• **Carbon:** Hamare shareer, khane aur pencil ki lead (graphite) mein hota hai.\n"
           "• **Chlorine:** Peene ke paani ke keede maar kar use saaf banane ke liye use hota hai.\n"
           "• **Iodine:** Chot lagne par antiseptic tincture ke roop mein lagaya jaata hai.\n\n"
           "💡 **Khaas baatein:** Metals malleable aur ductile hote hain. Non-metals brittle hote hain!",
        keywords=["metal", "metals", "nonmetal", "nonmetals", "non-metal", "non-metals", "dhaatu", "dhatu", "adhaatu",
                  "importance of metals and non-metals in daily life", "importance of metals and non-metals",
                  "importance of metals", "importance of non-metals", "daily life", "iron", "copper", "aluminium",
                  "gold", "oxygen", "nitrogen", "chlorine", "iodine", "malleability", "ductility", "sonorous"]),
}

HOME_ACTIVITIES = {
    "cabbage": dict(
        title_en="Red cabbage pH indicator", title_hi="Laal patta-gobhi pH indicator",
        en="With an adult: boil red cabbage leaves, let the purple water cool, then add a few drops of lemon juice "
           "(turns pink/red) or baking soda solution (turns blue/green). You made your own pH indicator!",
        hi="Kisi bade ke saath: laal patta-gobhi ke patte ubaalo, jamuni paani thanda karo, phir usme nimbu ka ras "
           "(gulabi/laal ho jaata hai) ya meetha soda ka ghol (neela/hara ho jaata hai) daalo. Tumne apna pH "
           "indicator bana liya!"),
    "volcano": dict(
        title_en="Baking soda & vinegar fizz", title_hi="Meetha soda aur sirka ka fizz",
        en="With an adult, outdoors or in a tray: add a spoon of baking soda to a cup, then pour in a little "
           "vinegar. The fizz is carbon dioxide gas! Wear safety glasses and never taste it.",
        hi="Kisi bade ke saath, bahar ya tray mein: ek cup mein ek chammach meetha soda daalo, phir thoda sirka "
           "daalo. Jo jhaag bante hain woh carbon dioxide gas hai! Safety chashma pehno aur kabhi chakhna nahi."),
    "states": dict(
        title_en="Ice, water and steam", title_hi="Barf, paani aur bhaap",
        en="Watch an ice cube melt in a bowl, and ask an adult to show steam rising from a kettle. Same water, "
           "three states! Never touch hot steam.",
        hi="Ek katori mein barf ko pighalte dekho, aur kisi bade se kaho ki kettle se nikalti bhaap dikhaye. "
           "Wahi paani, teen avasthayein! Garam bhaap ko kabhi mat chhuo."),
}

# ----------------------------------------------------------------------------- quiz
QUIZ = [
    dict(subject="Human body", q_en="Which organ pumps blood around the body?", q_hi="Kaun sa organ poore sharir mein khoon pump karta hai?",
         options=["Brain (Dimaag)", "Heart (Dil)", "Liver (Jigar)", "Kidney (Gurda)"], answer=1,
         ex_en="The heart is a muscle that pumps blood.", ex_hi="Dil ek muscle hai jo khoon pump karta hai."),
    dict(subject="Human body", q_en="Which organs help us breathe?", q_hi="Kaun se organs saans lene mein help karte hain?",
         options=["Lungs (Fefde)", "Stomach (Pet)", "Intestines (Aant)", "Kidneys (Gurde)"], answer=0,
         ex_en="Lungs take in oxygen and send out carbon dioxide.", ex_hi="Fefde oxygen lete hain aur carbon dioxide bahar nikalte hain."),
    dict(subject="Human body", q_en="How many bones does an adult human have?", q_hi="Ek bade insaan mein kitni haddiyan hoti hain?",
         options=["106", "206", "306", "56"], answer=1,
         ex_en="Adults have 206 bones.", ex_hi="Bade insaan mein 206 haddiyan hoti hain."),
    dict(subject="Physics", q_en="On Earth (ignoring air), which launch angle sends a ball the farthest?",
         q_hi="Earth par (hawa ko ignore karein) kaun sa angle gend ko sabse door bhejta hai?",
         options=["15°", "45°", "75°", "90°"], answer=1,
         ex_en="45° gives the maximum range because sin(2θ) is biggest there.",
         ex_hi="45° par range sabse zyada hoti hai kyunki wahan sin(2θ) sabse bada hota hai."),
    dict(subject="Physics", q_en="Voltage stays the same but resistance doubles. What happens to the current?",
         q_hi="Voltage same rehta hai lekin resistance double ho jaata hai. Current ka kya hoga?",
         options=["Doubles (Double)", "Halves (Aadha)", "Stays the same (Same)", "Becomes zero (Zero)"], answer=1,
         ex_en="I = V / R, so doubling R halves I.", ex_hi="I = V / R, isliye R double hone par I aadha ho jaata hai."),
    dict(subject="Physics", q_en="What happens to a pendulum's time period if the string gets longer?",
         q_hi="Agar pendulum ka dhaaga lamba ho jaaye toh uske time period ka kya hoga?",
         options=["Gets longer (Badhta hai)", "Gets shorter (Ghatta hai)", "Stays the same (Same)", "It stops (Ruk jaata hai)"], answer=0,
         ex_en="T = 2π√(L/g), so bigger L means bigger T.", ex_hi="T = 2π√(L/g), isliye L badhne par T badhta hai."),
    dict(subject="Physics", q_en="Light bending as it goes from air into water is called...",
         q_hi="Hawa se paani mein jaate waqt roshni ke mudne ko kya kehte hain?",
         options=["Reflection", "Refraction", "Absorption", "Evaporation"], answer=1,
         ex_en="Bending of light between materials is refraction.", ex_hi="Alag padarthon ke beech roshni ka mudna refraction hai."),
    dict(subject="Chemistry", q_en="How many protons does an oxygen atom have?", q_hi="Oxygen atom mein kitne protons hote hain?",
         options=["6", "8", "16", "2"], answer=1,
         ex_en="Oxygen's atomic number is 8, so it has 8 protons.", ex_hi="Oxygen ka atomic number 8 hai, isliye 8 protons hote hain."),
    dict(subject="Chemistry", q_en="A substance with pH 2 is...", q_hi="pH 2 wala padarth kaisa hota hai?",
         options=["A strong acid (Tez acid)", "Neutral", "A strong base (Tez base)", "Salt (Namak)"], answer=0,
         ex_en="Low pH means acidic.", ex_hi="Kam pH matlab acidic."),
    dict(subject="Chemistry", q_en="In which state of matter do particles move fastest and spread out the most?",
         q_hi="Kis avastha mein particles sabse tez chalte aur sabse zyada faile hote hain?",
         options=["Solid", "Liquid", "Gas", "Ice (Barf)"], answer=2,
         ex_en="Gas particles are far apart and move quickly.", ex_hi="Gas ke particles door-door hote hain aur tezi se chalte hain."),
    dict(subject="Chemistry", q_en="Water (H₂O) is made of which atoms?", q_hi="Paani (H₂O) kin atoms se bana hai?",
         options=["2 Hydrogen + 1 Oxygen", "2 Oxygen + 1 Hydrogen", "1 Carbon + 2 Oxygen", "1 Sodium + 1 Chlorine"], answer=0,
         ex_en="H₂O means two hydrogen atoms and one oxygen atom.", ex_hi="H₂O matlab do hydrogen aur ek oxygen atom."),
    dict(subject="Mathematics", q_en="In a right-angled triangle with legs a=3 cm and b=4 cm, what is the hypotenuse c?",
         q_hi="Right triangle mein agar a=3 cm aur b=4 cm hai, toh hypotenuse c kitna hoga?",
         options=["5 cm", "7 cm", "12 cm", "25 cm"], answer=0,
         ex_en="By Pythagoras theorem, c² = 3² + 4² = 9 + 16 = 25, so c = 5 cm.",
         ex_hi="Pythagoras pramey se, c² = 3² + 4² = 9 + 16 = 25, isliye c = 5 cm."),
    dict(subject="Mathematics", q_en="What is the area of a circle with radius r = 7 cm? (Use π ≈ 22/7)",
         q_hi="Agar radius r = 7 cm hai toh circle ka kshetraphal (area) kya hoga? (π ≈ 22/7 lein)",
         options=["44 cm²", "154 cm²", "49 cm²", "88 cm²"], answer=1,
         ex_en="Area = πr² = (22/7) × 7 × 7 = 154 cm².", ex_hi="Area = πr² = (22/7) × 7 × 7 = 154 cm²."),
    dict(subject="Mathematics", q_en="Solve the linear equation for x: 2x + 6 = 16",
         q_hi="Linear equation mein x ka maan nikalein: 2x + 6 = 16",
         options=["x = 5", "x = 10", "x = 8", "x = 4"], answer=0,
         ex_en="Subtract 6 from both sides: 2x = 10, then divide by 2: x = 5.",
         ex_hi="Dono taraf se 6 ghatayein: 2x = 10, phir 2 se divide karein: x = 5."),
]

# ----------------------------------------------------------------------------- mathematics (Class 1 to 8)
MATH_TOPICS = {
    "circle": dict(
        title_en="Circle (Perimeter & Area)", title_hi="Vritt / Circle (Paridhi & Kshetraphal)",
        en="A circle is a round 2D shape. The distance around it is circumference C = 2πr. The space inside is area A = πr².",
        hi="Circle ek gol 2D shape hai. Iske bahar ka ghera circumference C = 2πr hota hai aur andar ki jagah area A = πr² hoti hai.",
        formula="C = 2πr  •  Area = πr²",
        keywords=["circle", "vritt", "radius", "diameter", "circumference", "area", "pi", "perimeter"]),
    "rectangle": dict(
        title_en="Rectangle (Perimeter, Area & Diagonal)", title_hi="Aayat / Rectangle (Perimeter, Area & Diagonal)",
        en="A rectangle has 4 right angles. Opposite sides are equal. Perimeter is 2(l + w), Area is l × w, and diagonal is √(l² + w²).",
        hi="Rectangle mein aamne-saamne ki sides barabar hoti hain. Perimeter 2(l + w), Area l × w, aur diagonal √(l² + w²) hota hai.",
        formula="P = 2(l + w)  •  Area = l × w  •  d = √(l² + w²)",
        keywords=["rectangle", "aayat", "perimeter", "length", "width", "diagonal", "area"]),
    "triangle": dict(
        title_en="Triangle (Area = ½ × b × h)", title_hi="Tribhuj / Triangle (Area = ½ × b × h)",
        en="A triangle has 3 sides and 3 angles. The area inside is half of base times perpendicular height (A = ½ × b × h).",
        hi="Triangle mein 3 sides hoti hain. Iska kshetraphal (area) aadha guna base guna height (½ × b × h) hota hai.",
        formula="Area = ½ × base × height",
        keywords=["triangle", "tribhuj", "base", "height", "area", "hypotenuse"]),
    "cylinder": dict(
        title_en="3D Cylinder (Surface Area & Volume)", title_hi="3D Belan / Cylinder (Surface Area & Volume)",
        en="A cylinder has circular bases. Volume is πr²h, curved surface area is 2πrh, and total surface area is 2πr(r + h).",
        hi="Cylinder (belan) mein do circular bases hote hain. Volume πr²h aur curved surface area 2πrh hota hai.",
        formula="Volume = πr²h  •  CSA = 2πrh  •  TSA = 2πr(r + h)",
        keywords=["cylinder", "belan", "volume", "surface area", "radius", "height", "solid", "mensuration"]),
    "pythagoras": dict(
        title_en="Pythagoras Theorem (a² + b² = c²)", title_hi="Pythagoras Pramey (a² + b² = c²)",
        en="In any right-angled triangle, the square of the hypotenuse equals the sum of squares of the other two sides (a² + b² = c²).",
        hi="Kisi bhi samkon tribhuj (right triangle) mein hypotenuse ka square baaki do sides ke square ke jod ke barabar hota hai.",
        formula="a² + b² = c²  ➔  c = √(a² + b²)",
        keywords=["pythagoras", "theorem", "hypotenuse", "triplet", "right triangle", "karn", "pramey"]),
    "fractions": dict(
        title_en="Visual Fractions, Decimals & Percentages", title_hi="Bhinn / Fractions, Decimals & Percentages",
        en="A fraction represents equal parts of a whole (like pizza slices). For example, 3/8 = 0.375 = 37.5%.",
        hi="Fraction kisi poori cheez ke barabar hisson ko darshata hai (jaise pizza ke slices). Jaise 3/8 = 0.375 = 37.5%.",
        formula="Fraction = Numerator / Denominator  ➔  Percentage = (n/d) × 100%",
        keywords=["fraction", "bhinn", "percentage", "decimal", "ratio", "pizza", "numerator", "denominator"]),
    "algebra": dict(
        title_en="Linear Equations & Balance Scale (ax + b = c)", title_hi="Samikaran / Linear Equations (ax + b = c)",
        en="Think of an algebraic equation as a balancing scale. Perform identical operations on both sides to solve for x.",
        hi="Equation ko ek tarazu ki tarah samjhein. Dono taraf ek jaisa operation karke x ka sahi maan nikalein.",
        formula="ax + b = c  ➔  ax = c - b  ➔  x = (c - b) / a",
        keywords=["algebra", "equation", "samikaran", "variable", "linear", "solve", "balance", "scale"]),
    "counting": dict(
        title_en="🔢 Counting 1 to 10 (Apples & Stars)", title_hi="🔢 Ginti 1 se 10 (Seb aur Taare)",
        en="Count along with juicy red apples and glowing yellow stars! 1, 2, 3, 4, 5, 6, 7, 8, 9, 10! Each number represents one more object.",
        hi="Lal-lal seb aur chamakte sitaron ke saath ginti seekho! 1, 2, 3, 4, 5, 6, 7, 8, 9, 10! Har number ek naye object ko darshata hai.",
        formula="1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
        keywords=["count", "counting", "ginti", "number", "numbers", "apple", "apples", "seb", "star", "one", "two", "three"]),
    "shapes": dict(
        title_en="🔴 Basic Shapes (Circle, Square, Triangle, Star)", title_hi="🔴 Aakaar / Basic Shapes (Circle, Square, Triangle)",
        en="Shapes are all around us! A circle is round like a clock, a square has 4 equal sides like a slice of bread, a triangle has 3 sides like pizza, and a star has 5 glowing points!",
        hi="Aakaar humare aas-paas hain! Circle gol hota hai jaise ghadi, square ke 4 barabar kone hote hain jaise bread, triangle ke 3 kone hote hain jaise samosa, aur star ke 5 kone hote hain!",
        formula="Circle (0 sides) • Square (4 sides) • Triangle (3 sides) • Star (5 points)",
        keywords=["shape", "shapes", "circle", "square", "triangle", "star", "aakaar", "varg", "tribhuj", "gol"]),
    "candy_addition": dict(
        title_en="🍬 Visual Candy Addition (Combining Groups)", title_hi="🍬 Jod / Candy Addition (Jodna)",
        en="Addition is putting two groups of things together! If you have 2 candies and a friend gives you 3 more candies, you have 2 + 3 = 5 sweet treats!",
        hi="Jod (addition) ka matlab do cheezon ke samooh ko ikattha karna hota hai! Agar tumhare paas 2 toffee hain aur 3 aur mil jayein, toh 2 + 3 = 5 toffee ban jaati hain!",
        formula="a + b = Total Sum",
        keywords=["addition", "add", "plus", "jod", "jodna", "candy", "candies", "sum", "total"]),
}

# ----------------------------------------------------------------------------- general science (trees & animals)
NATURE_TOPICS = {
    "tree_parts": dict(
        title_en="🌳 Parts of a Tree & Plant (Roots, Stem, Leaves)",
        title_hi="🌳 Ped aur Paudhe ke Hisse (Jad, Tana, Patti)",
        en="A tree is a living organism with specialized parts: Roots anchor the tree and drink water from the soil; the Trunk and Branches give support and transport sap; Leaves catch sunlight to make food; and Flowers develop into Fruits with Seeds.",
        hi="Ped (tree) ek jeevit prani hai: Jado (roots) ped ko zameen mein thame rakhti hain aur paani peeti hain; Tana (trunk) sahara deta hai aur poshan pahunchata hai; Pattiyan (leaves) dhoop se khana banati hain; aur Phool phal aur beej banate hain.",
        formula="Tree Anatomy: Roots ➔ Trunk ➔ Branches ➔ Leaves ➔ Flowers & Fruits",
        keywords=["tree", "trees", "plant", "plants", "ped", "paudha", "paudhe", "roots", "stem", "leaves", "leaf", "branches", "trunk", "flower", "fruit", "jad", "tana", "patti", "botany", "nature"]),
    "photosynthesis": dict(
        title_en="☀️ Photosynthesis (How Trees Make Food)",
        title_hi="☀️ Prakash Sanshleshan (Pattiyan Khana Kaise Banati Hain)",
        en="Photosynthesis is the magical process where green leaves use Sunlight, Carbon Dioxide (CO2) from the air, and Water (H2O) from the roots to make Glucose sugar (food) and release fresh Oxygen (O2) for all of us to breathe!",
        hi="Photosynthesis woh jaadui kriya hai jismein hari pattiyan dhoop (sunlight), hawa se carbon dioxide (CO2) aur zameen se paani (H2O) lekar glucose (khana) banati hain aur humare saans lene ke liye taaza oxygen (O2) chhodti hain!",
        formula="6CO₂ + 6H₂O + Sunlight ➔ C₆H₁₂O₆ (Glucose) + 6O₂ (Oxygen)",
        keywords=["photosynthesis", "prakash sanshleshan", "chlorophyll", "green leaves", "sunlight", "carbon dioxide", "oxygen", "plant food", "stomata", "glucose"]),
    "butterfly_lifecycle": dict(
        title_en="🦋 Life Cycle of a Butterfly (Metamorphosis)",
        title_hi="🦋 Titli Ka Jeevan Chakra (Metamorphosis)",
        en="A butterfly undergoes a remarkable complete metamorphosis in 4 stages: 1. Egg laid on a leaf ➔ 2. Caterpillar (larva) that eats and grows ➔ 3. Chrysalis (pupa/cocoon) where it transforms ➔ 4. Adult Butterfly with colourful wings!",
        hi="Titli 4 khoobsurat charno mein poori tarah badalti hai: 1. Patti par Chhota Anda (Egg) ➔ 2. Bhookha Caterpillar (Kida) ➔ 3. Chrysalis (Cocoon) jismein badlaav hota hai ➔ 4. Sundar Pankhon Wali Badi Titli (Butterfly)!",
        formula="Egg ➔ Caterpillar (Larva) ➔ Chrysalis (Pupa) ➔ Adult Butterfly",
        keywords=["butterfly", "titli", "caterpillar", "chrysalis", "cocoon", "pupa", "larva", "metamorphosis", "life cycle", "insect"]),
    "frog_lifecycle": dict(
        title_en="🐸 Life Cycle of a Frog (Tadpole to Frog)",
        title_hi="🐸 Mendhak Ka Jeevan Chakra (Tadpole se Mendhak)",
        en="Frogs are amphibians that start life in water! The mother frog lays jelly eggs in water. They hatch into Tadpoles with tails and gills like fish. Gradually they grow back legs, then front legs, absorb their tail, develop lungs, and hop onto land as Adult Frogs!",
        hi="Mendhak (frog) jal-thalchar (amphibian) hai! Paani mein jelly ande hote hain jinse machhli jaisa Tadpole nikalta hai. Dheere-dheere uske pair nikalte hain, poonchh gayab hoti hai, fefde bante hain aur woh koodne wala mendhak ban jaata hai!",
        formula="Frog Eggs ➔ Tadpole (Water/Gills) ➔ Froglet ➔ Adult Frog (Land/Lungs)",
        keywords=["frog", "frogs", "mendhak", "tadpole", "amphibian", "froglet", "metamorphosis", "life cycle", "water animal"]),
    "animal_diets": dict(
        title_en="🦁 Animal Diets: Herbivores, Carnivores & Omnivores",
        title_hi="🦁 Jaanwaron Ka Khana: Shakahari, Mansahari aur Sarvahari",
        en="Animals eat different foods based on their body design: 1. Herbivores (cows, deer, rabbits) eat plants and grass. 2. Carnivores (lions, tigers, eagles) hunt and eat meat. 3. Omnivores (bears, crows, humans) eat both plants and meat!",
        hi="Jaanwar alag-alag khana khate hain: 1. Shakahari (Herbivores jaise gaay, hiran) ped-paudhe aur ghaas khate hain. 2. Mansahari (Carnivores jaise sher, baagh) maans khate hain. 3. Sarvahari (Omnivores jaise bhalu, kauwa, insaan) dono khate hain!",
        formula="Herbivore (Plants) • Carnivore (Meat) • Omnivore (Both)",
        keywords=["herbivore", "carnivore", "omnivore", "shakahari", "mansahari", "sarvahari", "animal diet", "animals", "animal", "jaanwar", "deer", "lion", "tiger", "bear"]),
    "food_chain": dict(
        title_en="🌱 The Forest Food Chain & Ecosystem",
        title_hi="🌱 Jungle Ki Aahar Shrinkhla (Food Chain)",
        en="All living things are connected in a food chain! The Sun gives energy to Plants (Producers). Deer or Rabbits (Primary Consumers) eat the grass. A Lion (Apex Predator) eats the deer. When animals pass away, Fungi and Bacteria (Decomposers) return nutrients to the soil for new trees to grow!",
        hi="Sabhi jeev aahar shrinkhla (food chain) se jude hain! Suraj ki dhoop se Paudhe (Producers) bante hain. Hiran ya khargosh ghaas khate hain. Sher unka shikaar karta hai. Baad mein mushrooms (decomposers) mitti ko poshan lautate hain jisse naye ped ug sakein!",
        formula="Sun ➔ Producer (Plant) ➔ Herbivore (Deer) ➔ Predator (Lion) ➔ Decomposer (Soil)",
        keywords=["food chain", "food web", "producer", "consumer", "predator", "ecosystem", "aahar shrinkhla", "forest", "jungle", "wildlife", "grass", "deer", "lion", "decomposer"]),
    "cute_animals": dict(
        title_en="🐶 Animals & Their Babies (Dog, Cat, Cow, Lion)",
        title_hi="🐶 Jaanwar aur Unke Bachhe (Puppy, Kitten, Bachhda)",
        en="Animals take care of their cute babies: Dogs have puppies that love to wag tails, cats have soft purring kittens, cows give milk to baby calves, and lions raise strong little cubs!",
        hi="Jaanwar apne pyare bachhon ka dhyan rakhte hain: Kutta puppy ke saath khelta hai, billi ke soft kittens hote hain, gaay bachhde ko doodh deti hai, aur sher ke shavak (cubs) hote hain!",
        formula="Parent ➔ Baby (Dog & Puppy • Cat & Kitten • Cow & Calf • Lion & Cub)",
        keywords=["animal", "animals", "baby", "puppy", "kitten", "dog", "cat", "cow", "lion", "cub", "jaanwar", "bachha", "kutta", "billi", "gaay"]),
    "seed_growth": dict(
        title_en="🌱 Seed to Plant: How Seeds Grow",
        title_hi="🌱 Beej se Paudha Kaise Banta Hai",
        en="A plant starts as a tiny seed asleep in warm soil. With water and warm sunshine, baby roots grow down to drink water and a bright green sprout shoots up to make green leaves and flowers!",
        hi="Paudha ek chhote beej se shuru hota hai. Paani aur dhoop milne par jad zameen mein jaati hai aur ek chhota ankur bahar nikal kar hari pattiyan aur phool banata hai!",
        formula="Seed in Soil ➔ Roots ➔ Green Sprout ➔ Stem & Leaves ➔ Flower",
        keywords=["seed", "sprout", "grow", "growth", "plant", "beej", "ankur", "soil", "mitti", "sunflower", "flower"]),
    "water_cycle": dict(
        title_en="💧 The Water Cycle (Sun, Clouds & Rain)",
        title_hi="💧 Jal Chakra (Dhoop, Baadal aur Baarish)",
        en="The Sun heats ocean and river water, turning it into invisible water vapour (evaporation). High in the sky it cools into clouds (condensation), and when full, drops fall as rain (precipitation)!",
        hi="Suraj ki garmi se paani bhaap bankar aasman mein jaata hai (evaporation). Wahan thanda hokar baadal bante hain (condensation), aur phir baarish bankar zameen par baraste hain (precipitation)!",
        formula="Evaporation ➔ Condensation (Clouds) ➔ Precipitation (Rain) ➔ Collection",
        keywords=["water cycle", "water", "cycle", "rain", "clouds", "evaporation", "jal chakra", "baarish", "baadal", "paani"]),
}

# ----------------------------------------------------------------------------- hinglish helpers
GREETINGS = {"hi", "hello", "hey", "namaste", "namaskar", "hii", "hiii", "yo", "good morning", "good evening"}

EXAMPLES = {
    "en": ["What does the heart do?", "Show me the lungs", "Explain the pendulum", "What is an atom of oxygen?",
           "Why does a straw look bent in water?"],
    "hi": ["Dil kya kaam karta hai?", "Fefde dikhao", "Pendulum samjhao", "Oxygen atom kya hota hai?",
           "Paani mein straw tedhi kyun dikhti hai?"],
}
