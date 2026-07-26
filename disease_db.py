# ============================================================
# disease_db.py
# AgriLens AI - Disease Database
# Language: Simple farmer-friendly (primary school level)
# Updated: Gray Leaf Spot removed, Maize Streak Disease added
# Urgency: Based on disease severity NOT model confidence
# MSD is always RED - viral, no cure, spreads fast
# ============================================================

DISEASE_INFO = {

    # ─────────────────────────────────────────────────────────
    # 1. COMMON RUST
    # Urgency: YELLOW - fungal, curable if caught early
    # ─────────────────────────────────────────────────────────
    "Corn_Common_Rust": {
        "urgency":       "yellow",
        "urgency_label": "Treat Soon — This Week",
        "urgency_color": "#d97706",
        "urgency_icon":  "🟡",
        "spread_note":   "Spreads fast in cool, wet weather. Act before it covers your farm.",

        "english": {
            "name": "Common Rust",
            "what_it_is": "A fungal disease that creates rusty orange spots on maize leaves. It spreads quickly in humid weather but can be controlled if you act early.",
            "symptoms": "Look for small orange or brown powder-like spots on the leaves. The spots may spread and cover more of the leaf if not treated.",
            "what_to_do": "Remove badly infected leaves right away. Give your plants more space so air can pass between them. Avoid watering leaves late in the evening — wet leaves overnight make the disease spread faster. Apply a recommended fungicide early when you first see the spots.",
            "prevention": "Use disease-resistant seeds when planting. Avoid using too much nitrogen fertilizer as it makes the disease spread faster. Always clean your farm tools before moving from one part of the farm to another.",
            "extension_note": "Common Rust responds well to early fungicide application. Advise farmer to apply at first sign of infection. Recommend resistant varieties for next season. Monitor humidity levels and plant spacing."
        },

        "pidgin": {
            "name": "Common Rust",
            "what_it_is": "Na fungus sickness wey dey put orange-brown powder spots for maize leaf. E dey spread fast when weather dey wet and cold.",
            "symptoms": "Check your leaf — you go see small orange-brown powder spots. If you no treat am early, e go spread cover plenty leaf.",
            "what_to_do": "Cut the bad leaves comot sharp sharp. Give your plants more space so air go pass between dem. No water the leaves for night — wet leaf overnight dey help the sickness spread. Buy fungicide from your agro-dealer and spray am when you first see the spots.",
            "prevention": "Plant seed wey no dey sick easy. No use too much nitrogen fertilizer. Always clean your farm tools before you move from one area to another.",
            "extension_note": "Common Rust dey respond well to early fungicide spray. Tell farmer make e spray when e first see the spots. Recommend resistant varieties for next season."
        },

        "yoruba": {
            "name": "Arun Afefe Agbado",
            "what_it_is": "Arun olu ni eyi to n fa awon ami pupa-brown lori ewe agbado. O n taran kiakia nigba ojo ati otutu.",
            "symptoms": "Wa awon ami kekeke pupa tabi brown bi erupe lori ewe. Ti o ba taran, yoo bo opo ewe.",
            "what_to_do": "Ge awon ewe ti o buru ju kuro lesikseki. Fun awon irugbin aaye to to ki afefe le san. Ma dun omi loru — ewe tutu loru n je ki arun na taran sii. Lo oogun ti agro-dealer gba lati fun ewe.",
            "prevention": "Gbin irugbin to lera si arun. Ma lo ajile nitrogen pupopo. Se imototo ise oko re nigbagbogbo.",
            "extension_note": "Common Rust n dahun si oogun ti a lo ni ibere. So fun agbe ki o lo oogun nigba ti o koko ri awon ami. Gba irugbin to lera lati gbin ni akoko to n bo."
        },

        "hausa": {
            "name": "Tsatsa na Masara",
            "what_it_is": "Cuta ce ta fungus da ke sanya tabo masu launin orange-ruwan kasa a ganyen masara. Tana yada da sauri a lokacin sanyi da damina.",
            "symptoms": "Duba ganye — za ka ga kananan tabo masu kama da foda orange ko ruwan kasa. Idan ba a bi da magani da wuri ba, za ta yadu ta rufe duk ganye.",
            "what_to_do": "Yanke ganyen da suka kamu sosai nan take. Ba wa shuke-shuken sarari don iska ta wuce tsakaninsu. Kada ka shayar da daddare — ganye mai danshi dare na taimaka wa cutar yaduwa. Sayo maganin fungus daga wurin mai kayayyakin noma ka fesa shi da wuri.",
            "prevention": "Shuka iri mai juriya ga cuta. Kar ka yi amfani da taki nitrogen mai yawa. Tsaftace kayan aikin gonarku koyaushe.",
            "extension_note": "Common Rust na amsa wa maganin fungus da aka yi amfani da shi da wuri. Shawarci manomi ya yi fesa da zarar ya ga alamu. Ba da shawarar iri mai juriya a kaka mai zuwa."
        },

        "igbo": {
            "name": "Oria Rust nke Oka",
            "what_it_is": "Oria ero bu nke na-eme ka akara orange-brown dika ntu puta n'akwukwo oka. O na-agbasa oge ojii na ozuzo.",
            "symptoms": "Lelee akwukwo — i huu obere akara orange ma obu brown dika ntu. Odi mma i lara izu, oga-ekpuchi akwukwo otutu.",
            "what_to_do": "Wepu akwukwo ndi oria ozugbo. Nye osisi gi ohere ikuku ibata n'etiti ha. Ekwesigh i poduo mmiri n'abalii — akwukwo ojii n'abalii na-enyere oria aka. Zuta ogwu fungus n'ulo ahia agro wee gee oge i huu akara mbua.",
            "prevention": "Kuo mkpuru nke na-eguzogide oria. Eji ajile nitrogen aruo olu oke. Hichapuo ihe fara n'ubi mgbe nile.",
            "extension_note": "Common Rust na-anabata ogwu fungus eji n'oge mbu. Gwa onye ubi ka o gee ogwu ozugbo o huu akara. Nyocha mkpuru na-eguzogide maka ohu ọhụrụ."
        },

        "severity": "Medium",
        "color":    "#d97706",
        "accent":   "#fffbeb",
        "border":   "#fde68a"
    },

    # ─────────────────────────────────────────────────────────
    # 2. NORTHERN CORN LEAF BLIGHT
    # Urgency: YELLOW to RED depending on spread
    # Default: YELLOW - fungal, treatable
    # ─────────────────────────────────────────────────────────
    "Corn_Northern_Leaf_Blight": {
        "urgency":       "yellow",
        "urgency_label": "Treat Immediately This Week",
        "urgency_color": "#d97706",
        "urgency_icon":  "🟡",
        "spread_note":   "Can reduce your harvest by up to 50% if not treated quickly.",

        "english": {
            "name": "Northern Corn Leaf Blight",
            "what_it_is": "A fungal disease that causes long brown or grey spots on maize leaves. It starts from the bottom leaves and moves upward. It can destroy a large part of your harvest if ignored.",
            "symptoms": "Look for long spots shaped like a cigar on the leaves. The spots are brown or grey and the leaf starts drying from the bottom of the plant upward.",
            "what_to_do": "Remove heavily infected leaves as soon as possible. Do not move from infected plants to healthy ones without first cleaning your hands and tools. Reduce crowding on your farm so air can pass freely between plants. Ask your local agro-dealer or extension officer for a recommended fungicide and apply it early.",
            "prevention": "Plant resistant maize varieties. Rotate your crops — do not plant maize on the same land every season. After harvest, remove and destroy old infected plant materials. Do not leave dead crop residue on the farm.",
            "extension_note": "Northern Corn Leaf Blight is caused by Exserohilum turcicum. Recommend scouting at V6-V8 growth stage. Fungicide threshold is when 5 percent or more of upper canopy leaves show lesions. Advise crop rotation and use of certified resistant varieties next season."
        },

        "pidgin": {
            "name": "Northern Corn Leaf Blight",
            "what_it_is": "Na fungus sickness wey dey cause long brown or grey marks for maize leaf. E dey start from the bottom leaves and dey go up. E fit destroy plenty of your harvest if you no do something fast.",
            "symptoms": "Look for long marks wey resemble cigar for the leaf. The marks dey brown or grey color and the leaf dey start dry from the bottom of the plant upward.",
            "what_to_do": "Cut the badly infected leaves comot sharp sharp. No move from sick plants to healthy ones without first washing your hands and tools. Give your plants more breathing space. Ask your agro-dealer or extension officer for the right fungicide and spray am early.",
            "prevention": "Plant maize wey no dey sick easy. Change the crop wey you plant every season — no plant maize for same ground every year. After harvest, clear all old infected plants comot from the farm.",
            "extension_note": "E happen because of Exserohilum turcicum fungus. Check farm at V6-V8 stage. If 5% or more of top leaves get lesions, spray immediately. Advise rotation and resistant varieties next season."
        },

        "yoruba": {
            "name": "Arun Blight Agbado Ariwa",
            "what_it_is": "Arun olu ni eyi to n fa awon ami gigun brown tabi grey lori ewe agbado. O n bere lati ewe isale o n goke. O le pa opo irugbin re run bi o ba gba akoko.",
            "symptoms": "Wa awon ami gigun bi siga lori ewe. Awon ami naa jẹ brown tabi grey, ewe si n gbẹ lati isale oke.",
            "what_to_do": "Ge awon ewe ti o buru ju kuro lesikẹsẹ. Ma lo ọwọ kanna lati ile arun de ile to dara laisi mimọ ọwọ ati ohun elo re. Fun aaye ki afefe le san. Beere lọwọ agro-dealer tabi oluko ọgbin fun oogun to yẹ, lo si ni kutukutu.",
            "prevention": "Gbin irugbin agbado to lera. Yi irugbin pada — ma gbin agbado ni ilẹ kanna ni gbogbo akoko. Lẹyin ikore, gba gbogbo egbin irugbin ti o ni arun kuro ni oko.",
            "extension_note": "O jẹ arun ti Exserohilum turcicum n fa. Ṣayẹwo ni V6-V8. Ti 5 ida ọgọrun tabi ju bẹ lọ ti ewe oke ba ni ami, lo oogun lesikẹsẹ. Gba irugbin to lera fun akoko to n bọ."
        },

        "hausa": {
            "name": "Ciwon Ganye na Arewa",
            "what_it_is": "Cuta ce ta fungus da ke haddasa dogayen tabo masu launin ruwan kasa ko toka a ganyen masara. Tana farawa daga ganyen kasa ta tafi sama. Idan ba a yi komai ba, za ta lalata yawan amfanin gonarku.",
            "symptoms": "Nemi dogayen tabo masu kama da sigari a ganye. Launinsu ruwan kasa ne ko toka, kuma ganye yana fara bushewa daga kasa zuwa sama.",
            "what_to_do": "Yanke ganyen da suka kamu sosai nan take. Kada ka tafi daga shuke wanda ya kamu zuwa wanda bai kamu ba ba tare da wanke hannunka da kayan aiki ba. Ba wa shuke-shuken sarari. Tambayi mai kayayyakin noma ko jami'in fadakarwa maganin da ya dace kuma ka yi amfani da shi da wuri.",
            "prevention": "Shuka masara mai juriya ga cuta. Canza amfanin gona kowane kaka — kada ka dasa masara a gonaki iri daya koyaushe. Bayan girbi, share dukkan tsofaffin shuke-shuken da suka kamu ka kore su daga gonar.",
            "extension_note": "Exserohilum turcicum ne ke haddasa wannan cuta. Duba gonar a V6-V8. Idan kashi 5 cikin dari ko fiye na ganyen sama suna da tabo, yi fesa nan take. Ba da shawarar juyawa da iri mai juriya a kaka mai zuwa."
        },

        "igbo": {
            "name": "Oria Akwukwo Oka Ugwu",
            "what_it_is": "Oria ero bu nke na-eme ka ogologo akara brown ma obu grey puta n'akwukwo oka. O na-amalite na akwukwo n'okpuru wee gaa elu. Oda ike imebi ihe i kuru ma i ghara ime ihe ngwa ngwa.",
            "symptoms": "Choo ogologo akara di ka siga n'akwukwo. Ha di brown ma obu grey, akwukwo si n'okpuru malite iko.",
            "what_to_do": "Wepu akwukwo ndi oria ozugbo. Eji aka ma obu ngwa oji aga n'osisi oria gaa n'osisi di mma enwegh isa aka. Nye osisi gi ohere ikuku ibata. Juo onye na-ere ihe ubi ma obu onye oru ugbo maka ogwu kwesiri, gee ya n'oge.",
            "prevention": "Kuo mkpuru oka na-eguzogide oria. Gbanwee ihe i na-akuo kwa ohu — akuodughi oka n'ala ahu kwa oge. Mgbe i sochara oba, wepu ma zuo ihe fara nile nwere oria n'ubi.",
            "extension_note": "Exserohilum turcicum ka na-akpata oria a. Lelee na V6-V8. Odi mma 5 pasent ma obu kariri nke akwukwo elu nwere akara, gee ogwu ozugbo. Nyocha mkpuru na-eguzogide maka ohu ọhụrụ."
        },

        "severity": "High",
        "color":    "#dc2626",
        "accent":   "#fef2f2",
        "border":   "#fca5a5"
    },

    # ─────────────────────────────────────────────────────────
    # 3. MAIZE STREAK DISEASE (MSD)
    # Urgency: ALWAYS RED - viral, no cure, spreads fast
    # Replaces Gray Leaf Spot
    # ─────────────────────────────────────────────────────────
    "Corn_Maize_Streak": {
        "urgency":       "high",
        "urgency_label": "CRITICAL — Remove Infected Plants Now",
        "urgency_color": "#dc2626",
        "urgency_icon":  "🔴",
        "spread_note":   "This is a viral disease. There is NO cure. Remove infected plants immediately to protect the rest of your farm.",

        "english": {
            "name": "Maize Streak Disease",
            "what_it_is": "This is a serious viral disease spread by tiny insects called leafhoppers. Once a plant is infected, there is no medicine that can cure it. The only way to protect your farm is to remove infected plants immediately and stop the insects from spreading it further.",
            "symptoms": "Look for yellow streaks running along the leaves. The plant stops growing well and becomes stunted. The leaves may look pale or washed out with yellow or white lines along them.",
            "what_to_do": "Remove infected plants from the farm completely — pull them out by the root and take them far away from your farm or burn them. Do not leave them on the ground near healthy plants. Control the small jumping insects (leafhoppers) that spread this disease by asking your agro-dealer for insect control spray. Do not replant maize immediately in a heavily infected area.",
            "prevention": "Plant maize varieties that are resistant to Maize Streak Disease — ask your agro-dealer for MSV-resistant seeds. Plant early in the season before leafhopper numbers are high. Keep your farm and surroundings clean and free of weeds where leafhoppers hide.",
            "extension_note": "Maize Streak Virus (MSV) is transmitted by the leafhopper Cicadulina mbila. There is no cure once infected. Recommend immediate removal of infected plants to reduce inoculum pressure. Advise use of MSV-resistant certified varieties. Early planting before peak leafhopper season reduces risk significantly. Insecticide seed treatment or early spray reduces vector population."
        },

        "pidgin": {
            "name": "Maize Streak Disease",
            "what_it_is": "Na serious virus sickness wey small insects wey dem dey call leafhoppers dey spread am. Once plant don kamu, no medicine fit cure am. The only way to protect your farm na to remove the sick plants immediately and stop the insects from spreading am further.",
            "symptoms": "Look for yellow lines wey dey run along the leaf. The plant go stop growing well and e go short. The leaves go look pale or wash-out with yellow or white lines on dem.",
            "what_to_do": "Remove the sick plants from the farm completely — pull dem comot from the root and carry dem far from your farm or burn dem. No leave dem near healthy plants. Control the small jumping insects (leafhoppers) — ask your agro-dealer for insect spray. No replant maize immediately for area wey the disease don spread well.",
            "prevention": "Plant maize wey dem call MSV-resistant — ask your agro-dealer for this seed. Plant early for the season before the insects don plenty. Keep your farm clean and remove weeds wey the insects dey hide inside.",
            "extension_note": "Maize Streak Virus (MSV) dey spread through leafhopper Cicadulina mbila. No cure once e kamu. Remove infected plants immediately. Advise MSV-resistant varieties. Early planting reduces risk. Insecticide seed treatment dey help reduce the insects."
        },

        "yoruba": {
            "name": "Arun Streak Agbado",
            "what_it_is": "Eyi jẹ arun ọlọjẹ to le pupọ ti awọn kokoro kekere ti a pe ni leafhoppers n tan kaakiri. Ni kete ti ọgbin ba ni arun, ko si oogun ti o le wosan. Ọna kan ṣoṣo lati daabobo oko rẹ ni lati yọ awọn ọgbin aisan kuro lesikẹsẹ.",
            "symptoms": "Wa awọn ila ofeefee ti n rin lẹba ewe. Ọgbin dẹkun idagba daradara o si dagba kekere. Ewe le ri pẹlẹ tabi ti ya pẹlu awọn laini ofeefee tabi funfun.",
            "what_to_do": "Yọ awọn ọgbin aisan kuro ninu oko patapata — fa wọn jade pẹlu gbongbo wọn ki o mu wọn jinna si oko tabi jona wọn. Maṣe fi wọn silẹ nitosi awọn ọgbin ilera. Beere lọwọ agro-dealer fun oogun ipakokoro lati pa awọn kokoro leafhoppers. Maṣe tun gbin agbado lesikẹsẹ ni agbegbe ti arun ti tan si.",
            "prevention": "Gbin agbado ti o lera si arun Streak — beere lọwọ agro-dealer fun irugbin MSV-resistant. Gbin ni ibẹrẹ akoko ṣaaju ki awọn kokoro to pọ. Jẹ ki oko rẹ mọ kuro ninu awọn èpo ti awọn kokoro n pamọ sinu.",
            "extension_note": "Maize Streak Virus (MSV) jẹ tan kaakiri nipasẹ leafhopper Cicadulina mbila. Ko si arowoto lẹhin ikolu. Yọ awọn ọgbin aisan kuro lesikẹsẹ. Gba irugbin MSV-resistant ti a fọwọsi. Gbingbin ni kutukutu n dinku ewu."
        },

        "hausa": {
            "name": "Ciwon Streak na Masara",
            "what_it_is": "Wannan cuta ce mai tsanani ta kwayar cuta da kananan kwari da ake kira leafhoppers ke yada ta. Da zarar shuka ta kamu, babu magani da zai warkar da ita. Hanyar da ta fi dacewa wajen kiyaye gonarku ita ce cirewa shuke-shuken da suka kamu nan take da kuma hana kwari yada cutar.",
            "symptoms": "Nemi layin rawaya da ke gudana a tsawon ganye. Shuka tana daina girma yadda yakamata kuma tana zama gajere. Ganyen na iya zama mai launi mai tsami ko fari tare da layuka masu rawaya ko fari a kansu.",
            "what_to_do": "Cire shuke-shuken da suka kamu daga gonar gaba daya — fitar da su daga cikin kasa kuma ka kai su nesa da gonar ko ka kone su. Kada ka bari su kusa da shuke-shuke masu lafiya. Sarrafa kananan kwarin leafhoppers — tambayi mai kayayyakin noma maganin kashe kwari. Kada ka sake dasa masara nan take a wuri da cutar ta bazu sosai.",
            "prevention": "Shuka masaran da aka fi sani da MSV-resistant — tambayi mai kayayyakin noma wannan iri. Dasa da wuri a kaka kafin kwarin ya yi yawa. Kiyaye gonarku da kewayenta daga ciyayi inda kwarin ke ɓuya.",
            "extension_note": "Maize Streak Virus (MSV) leafhopper Cicadulina mbila ke yada ta. Babu magani bayan kamuwa. Cire shuke-shuken da suka kamu nan take. Shawarci iri MSV-resistant. Dasa da wuri na rage haɗari. Maganin iri na insecticide na taimaka rage yawan kwari."
        },

        "igbo": {
            "name": "Oria Streak nke Oka",
            "what_it_is": "Nke a bu oria virus di egwu nke obere uke a na-akpo leafhoppers na-ebughariri. Ozugbo osisi akwusiri oria, enwegh ogwu nwere ike gwoo ya. Naanị ụzọ isi chebe ubi gi bu ibukwuo osisi oria ngwa ngwa ma gbochie uke n'ịgbasa ya.",
            "symptoms": "Choo ahịrị odo na-agba n'akwukwo. Osisi kwusiiri eto nke oma wee di obere. Akwukwo nwere ike di mfe ma obu cha cha nwere ahịrị odo ma obu ọcha n'ha.",
            "what_to_do": "Wepu osisi ndi oria n'ubi nile — dobe ha site n'mgbidi ha wee karia ha n'ebe dị anya n'ubi ma obu kuo ha oku. Akwusigh ha n'ebe osisi di mma dị. Chekwaa obere uke ndị leafhoppers — juo onye na-ere ihe ubi maka ogwu igbu uke. Akukodughi oka ngwa ngwa n'ubi ebe oria gbara ọsọ.",
            "prevention": "Kuo oka a na-akpo MSV-resistant — juo onye na-ere ihe ubi maka mkpuru a. Kuo n'oge mbu n'ohu tupu uke eruola oke. Hichapua ubi gi na gburugburu ya n'ahịhịa ebe uke na-etoi.",
            "extension_note": "Maize Streak Virus (MSV) leafhopper Cicadulina mbila na-ebufe ya. Enwegh ogwu mgbe oria eruola. Wepu osisi oria ozugbo. Nyocha mkpuru MSV-resistant nwere akwukwo nkwenye. Ikuo n'oge mbu na-ebelata ihe ize ndụ."
        },

        "severity": "Critical",
        "color":    "#991b1b",
        "accent":   "#fff1f2",
        "border":   "#fecdd3"
    },

    # ─────────────────────────────────────────────────────────
    # 4. HEALTHY PLANT
    # Urgency: GREEN - no action needed
    # ─────────────────────────────────────────────────────────
    "Corn_Healthy": {
        "urgency":       "none",
        "urgency_label": "Your Crop Looks Healthy",
        "urgency_color": "#16a34a",
        "urgency_icon":  "🟢",
        "spread_note":   "Keep up the good work. Monitor your farm regularly.",

        "english": {
            "name": "Healthy Plant",
            "what_it_is": "Good news! No signs of disease were found on this leaf. Your maize plant appears to be growing well.",
            "symptoms": "No signs of disease detected. Leaves look green and healthy with normal color and structure.",
            "what_to_do": "Continue your good farming practices. Check your farm every 3 to 5 days for early signs of disease. Keep plants well spaced so air can move freely. Water consistently and avoid waterlogging.",
            "prevention": "Keep using good seeds. Rotate your crops every season. Keep your farm clean and free of old plant residue. Monitor regularly and act early if you notice any changes.",
            "extension_note": "No intervention required at this time. Encourage farmer to maintain regular scouting routine every 3 to 5 days. Reinforce good agronomic practices including proper spacing, crop rotation, and timely fertilizer application."
        },

        "pidgin": {
            "name": "Healthy Plant",
            "what_it_is": "Good news! No disease sign dey this leaf. Your maize plant dey grow well well.",
            "symptoms": "No disease dey here. The leaf dey green and healthy with normal color and shape.",
            "what_to_do": "Continue the good farming work wey you dey do. Check your farm every 3 to 5 days. Give your plants enough space so air go pass well. Water am well — no allow the water stand for ground.",
            "prevention": "Continue using good seeds. Change the crop wey you plant every season. Keep your farm clean. Monitor regularly and act fast if you see any change.",
            "extension_note": "No action needed now. Encourage farmer to check farm every 3 to 5 days. Reinforce good practices — spacing, rotation, and fertilizer timing."
        },

        "yoruba": {
            "name": "Irugbin Ti O Ni Ilera",
            "what_it_is": "Iroyin rere! Ko si ami arun kankan lori ewe yii. Agbado rẹ dabi ẹnipe n dagba daradara.",
            "symptoms": "Ko si ami arun. Ewe wo alawọ ewe ati ilera pẹlu awọ deede ati eto deede.",
            "what_to_do": "Tẹsiwaju pẹlu iṣẹ oko rẹ ti o dara. Ṣayẹwo oko rẹ ni gbogbo ọjọ 3 si 5. Fun awọn irugbin aaye to to ki afẹfẹ le san. Dun omi daradara — maṣe jẹ ki omi duro lori ilẹ.",
            "prevention": "Tẹsiwaju lilo irugbin to dara. Yi irugbin pada ni gbogbo akoko. Jẹ ki oko rẹ mọ. Ṣayẹwo nigbagbogbo ki o si ṣe igbese ni kiakia bi o ba ri iyipada kankan.",
            "extension_note": "Ko si iṣẹ pataki lọwọlọwọ. Gba agbe niyanju lati ṣayẹwo oko ni gbogbo ọjọ 3 si 5. Ṣe alaye awọn iṣe ogbin to dara."
        },

        "hausa": {
            "name": "Lafiyayyiyar Shuka",
            "what_it_is": "Labari mai dadi! Babu alamun cuta a wannan ganye. Masarar ka tana girma sosai.",
            "symptoms": "Babu cuta a nan. Ganyen yana da kore kuma lafiyayye da launi na yau da kullum.",
            "what_to_do": "Ci gaba da ayyukan gona masu kyau. Duba gonarku kowace kwana 3 zuwa 5. Ba wa shuke-shuken sarari don iska ta wuce. Shayar da kyau — kar a bar ruwa ya tsaya a kasa.",
            "prevention": "Ci gaba da amfani da iri mai kyau. Canza amfanin gona kowane kaka. Kiyaye gonar daga tsafta. Kula koyaushe kuma a yi aiki da wuri idan ka ga wata canjin.",
            "extension_note": "Babu bukata na sa baki yanzu. Karfafa manomi ya duba gonar kowace kwana 3 zuwa 5. Karfafa ayyukan noma masu kyau."
        },

        "igbo": {
            "name": "Osisi Ahụike",
            "what_it_is": "Ọ dị mma! Enwegh ihe ọrịa achọtara n'akwukwo a. Oka gi na-eto nke oma.",
            "symptoms": "Enwegh oria ebe a. Akwukwo di ọcha na ahụike nwere agwa na nhazi nkịtị.",
            "what_to_do": "Gaa n'ihu na ihe ọma i na-eme n'ubi. Lelee ubi gi kwa ụbọchị 3 ruo 5. Nye osisi gi ohere ikuku ibata. Poduo mmiri nke oma — ezere ka mmiri kpuchie ala.",
            "prevention": "Gaa n'ihu iji mkpuru ọma. Gbanwee ihe i na-akuo kwa ohu. Hichapua ubi gi. Lelee mgbe nile ma mee ihe ngwa ngwa ma ọ bụrụ na i huu mgbanwe.",
            "extension_note": "Ọ dịghị mkpa ọ bụla ugbua. Kwalite onye ubi ka o lelee ubi kwa ụbọchị 3 ruo 5. Kwalite ọrụ ugbo ọma."
        },

        "severity": "None",
        "color":    "#16a34a",
        "accent":   "#f0fdf4",
        "border":   "#86efac"
    }
}

# ─── Label alias map ───────────────────────────────────────────
# Maps your model's output labels to DISEASE_INFO keys
# Update these when you retrain with MSD dataset
LABEL_ALIAS = {
    # Current model labels (before retraining)
    "Blight":                    "Corn_Northern_Leaf_Blight",
    "Common_Rust":               "Corn_Common_Rust",
    "Gray_Leaf_Spot":            "Corn_Maize_Streak",  # temporary mapping
    "Healthy":                   "Corn_Healthy",

    # Full name versions
    "Corn_Northern_Leaf_Blight": "Corn_Northern_Leaf_Blight",
    "Corn_Common_Rust":          "Corn_Common_Rust",
    "Corn_Maize_Streak":         "Corn_Maize_Streak",
    "Corn_Healthy":              "Corn_Healthy",

    # After retraining with MSD dataset
    "Maize_Streak":              "Corn_Maize_Streak",
    "MSD":                       "Corn_Maize_Streak",
}