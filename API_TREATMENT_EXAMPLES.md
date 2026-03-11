# Treatment API Response Examples

## /treatment-plan Endpoint Responses

### Example 1: Blight Disease Treatment Plan

```json
{
  "disease": "Blight",
  "disease_severity": "High - Requires Immediate Action",
  "recovery_time": "2-3 weeks with consistent treatment",
  
  "primary_pesticide": {
    "product": "Copper oxychloride 50% WP",
    "details": {
      "dosage": "2 to 2.5 g per liter of water",
      "water_requirement": "400-600 liters per hectare",
      "application_method": "Fine mist foliar spray covering both leaf surfaces uniformly",
      "best_time": "Early morning (6-9 AM) or late afternoon (4-7 PM)",
      "frequency": "Every 7 days",
      "duration": "2 to 3 sprays minimum",
      "safety": "Wear gloves, mask, boots, and long sleeves; minimum 7-day harvest interval",
      "storage": "Store in cool, dry place away from moisture"
    }
  },
  
  "alternative_pesticides": [
    {
      "name": "Chlorothalonil 75% WP",
      "dosage": "2 to 2.5 g per liter",
      "cost_indicator": "$",
      "effectiveness": "High",
      "note": "Broad-spectrum fungicide, effective for early blight"
    },
    {
      "name": "Mancozeb 75% WP",
      "dosage": "1.5 to 2 g per liter",
      "cost_indicator": "$",
      "effectiveness": "High",
      "note": "Protectant fungicide, best used preventively"
    },
    {
      "name": "Neem oil (Organic)",
      "dosage": "5 ml per liter + 1 ml soap per liter",
      "cost_indicator": "$",
      "effectiveness": "Medium (early stages)",
      "note": "Organic option, less harsh on environment"
    }
  ],
  
  "primary_fertilizer": {
    "product": "NPK 19:19:19 (Water-soluble)",
    "details": {
      "dosage": "5 g per liter for foliar spray",
      "water_requirement": "300-400 liters per hectare",
      "timing": "Apply 24 to 48 hours after pesticide spray",
      "application_method": "Fine spray covering all leaves, upper and lower surfaces",
      "goal": "Support recovery and encourage new healthy foliage growth",
      "repeat": "Every 10-12 days for 2-3 applications"
    }
  },
  
  "alternative_fertilizers": [
    {
      "name": "Calcium Nitrate + Potassium Sulfate",
      "dosage": "5 g calcium nitrate + 3 g potassium sulfate per liter",
      "timing": "2-3 days after fungicide",
      "note": "Strengthens cell walls, increases disease resistance"
    },
    {
      "name": "Foliar spray - NPK 19:19:19",
      "dosage": "5 g per liter",
      "timing": "24-48 hours after fungicide",
      "note": "Quick recovery support"
    }
  ],
  
  "equipment_needed": [
    "Knapsack sprayer (16-20 liters)",
    "Pruning shears",
    "Gloves and mask",
    "Measuring scale (0-5 g)",
    "Spray nozzle (fine mist type)"
  ],
  
  "preventive_measures": [
    "Remove infected leaves immediately",
    "Improve air circulation by pruning lower branches",
    "Avoid overhead irrigation - water at soil level only",
    "Sterilize pruning tools between cuts",
    "Remove and burn infected debris, never compost",
    "Maintain crop rotation (3-4 years)"
  ],
  
  "step_by_step_treatment": [
    "Step 1: IMMEDIATE - Remove all heavily infected leaves and destroy them away from the field (burn or bury deep). Do NOT compost.",
    "Step 2: Prepare spray solution - Fill tank with clean water, add Copper oxychloride 50% WP at 2 to 2.5 g per liter, mix thoroughly for 15 minutes.",
    "Step 3: Put on protective equipment - long sleeves, gloves, mask, boots, and eye protection.",
    "Step 4: Spray the entire canopy with fine mist coverage on both upper and lower leaf surfaces until near runoff. Avoid spraying in midday heat or strong wind.",
    "Step 5: Re-spray every 7 days for a minimum of 2-3 cycles, adjusting based on symptom reduction.",
    "Step 6: After 24-48 hours from last fungicide spray, apply NPK 19:19:19 foliar nutrition at 5 g per liter as recovery support.",
    "Step 7: Maintain proper drainage and avoid leaf wetness from overhead watering - water only at soil level in early morning.",
    "Step 8: Prune to improve air circulation - remove lower branches and thin dense foliage.",
    "Step 9: Monitor disease spread every 2-3 days using inspection cards or magnifying glass.",
    "Step 10: Once new growth appears healthy and disease stops spreading (3-5 days symptom-free), reduce spray frequency to maintenance schedule."
  ],
  
  "success_indicators": [
    "Lesion growth stops and turns brown",
    "New leaves emerge without spots",
    "Yellow halo around lesions disappears",
    "Leaf drop slows significantly"
  ],
  
  "key_precautions": [
    "Never mix copper fungicides with oil-based products",
    "Do not exceed recommended dosage",
    "Observe harvest interval (check label, typically 7-14 days)",
    "Use only in well-ventilated areas",
    "Wash hands, face, and exposed skin immediately after spraying"
  ]
}
```

---

### Example 2: Rust Disease Treatment Plan

```json
{
  "disease": "Rust",
  "disease_severity": "Medium-High - Needs Urgent Treatment",
  "recovery_time": "1-2 weeks with consistent treatment",
  
  "primary_pesticide": {
    "product": "Wettable sulfur 80% WDG (Primary)",
    "details": {
      "dosage": "2 g per liter of water",
      "water_requirement": "350-500 liters per hectare",
      "application_method": "Foliar spray during cool hours (early morning or after 4 PM)",
      "best_time": "Early morning (6-9 AM) or late evening (5-7 PM)",
      "frequency": "Every 7 to 10 days based on weather",
      "duration": "2 to 3 sprays, continue until new growth is symptom-free",
      "safety": "Do not mix with incompatible alkaline products; avoid mixing with oil-based sprays within 2 weeks",
      "ph_requirement": "Slightly acidic water (pH 6.5-7.0) for best effectiveness"
    }
  },
  
  "alternative_pesticides": [
    {
      "name": "Tebuconazole 25% EC",
      "dosage": "1 ml per 2 liters of water",
      "cost_indicator": "$$",
      "effectiveness": "Very High",
      "note": "Systemic fungicide, penetrates leaf tissue"
    },
    {
      "name": "Hexaconazole 5% EC",
      "dosage": "2 ml per liter",
      "cost_indicator": "$$",
      "effectiveness": "High",
      "note": "Contact and systemic action"
    },
    {
      "name": "Neem oil + Sulfur mixture (Organic)",
      "dosage": "5 ml neem + 2 g sulfur per liter",
      "cost_indicator": "$",
      "effectiveness": "Medium",
      "note": "Natural option with preventive properties"
    }
  ],
  
  "primary_fertilizer": {
    "product": "SOP (Potassium Sulfate) 0:0:50 or K-Nitrate",
    "details": {
      "dosage": "3 to 5 g per liter for foliar application",
      "water_requirement": "300-400 liters per hectare",
      "timing": "1 to 2 days after fungicide application",
      "application_method": "Fine foliar spray covering all leaf surfaces",
      "goal": "Improve disease stress tolerance and strengthen plant tissue",
      "repeat": "Every 10-14 days for 2-3 applications"
    }
  },
  
  "alternative_fertilizers": [
    {
      "name": "SOP (Potassium Sulfate) 0:0:50",
      "dosage": "3-5 g per liter foliar application",
      "timing": "1-2 days after fungicide",
      "note": "Improves disease resistance"
    },
    {
      "name": "Monopotassium Phosphate - MKP 0:52:34",
      "dosage": "4-6 g per liter",
      "timing": "2-3 days after fungicide",
      "note": "Boosts immunity and tissue strength"
    }
  ],
  
  "equipment_needed": [
    "Knapsack sprayer or backpack sprayer",
    "Sulfur powder dispenser or spray nozzle",
    "Protective gear (gloves, mask, protective suit)",
    "Measuring scale",
    "Spray timer or schedule chart"
  ],
  
  "preventive_measures": [
    "Avoid overhead watering - use drip irrigation",
    "Use disease-resistant plant varieties when possible",
    "Maintain proper row spacing (2-3 feet minimum)",
    "Prune lower leaves to improve air circulation",
    "Remove fallen leaves and debris immediately",
    "Clean and sterilize all tools regularly"
  ],
  
  "step_by_step_treatment": [
    "Step 1: Inspect the plant thoroughly - look for orange/rust-colored pustules on leaf undersides and yellow spots on upper surface.",
    "Step 2: Remove severely rusted leaves - carefully prune leaves with >50% coverage affected and destroy them away from field.",
    "Step 3: Prepare sulfur spray solution - Mix 2 g wettable sulfur per liter of clean water in a garden sprayer, stir well.",
    "Step 4: Equip with protective gear - gloves, mask, and protective clothing.",
    "Step 5: Spray during cool hours (early morning) - cover entire canopy uniformly, focusing on leaf undersides where rust develops.",
    "Step 6: Re-spray every 7-10 days after first application, monitoring weather patterns (increase frequency in high humidity).",
    "Step 7: One to two days after fungicide application, apply SOP 0:0:50 foliar feed at 3-5 g per liter to strengthen plant immunity.",
    "Step 8: Improve air circulation - prune lower leaves, space plants adequately, remove obstacles to airflow.",
    "Step 9: Change irrigation method to drip watering - keep foliage dry, especially during night hours.",
    "Step 10: Scout every 3-5 days for new pustule development; continue sprays until new growth emerges symptom-free for at least 1 week."
  ],
  
  "success_indicators": [
    "Orange pustules stop producing new spores",
    "Rust patches turn dark brown/black",
    "Yellow yellowing halts around rust spots",
    "New leaves emerge without rust symptoms",
    "Leaf drop significantly decreases"
  ],
  
  "key_precautions": [
    "Do not apply sulfur within 2 weeks of oil-based pesticides",
    "Temperature should be below 85°F for sulfur application",
    "Avoid mixing sulfur with alkaline materials",
    "Check product label for compatibility with other products",
    "Use only approved sulfur products for food crops"
  ],
  
  "important_notes": [
    "Begins in cool (50-75°F), wet weather favoring fungal growth",
    "Spread by infected plant material or wind-borne spores",
    "High humidity and poor air circulation accelerate spread",
    "Early detection and treatment are critical for control"
  ]
}
```

---

### Example 3: Powdery Mildew Treatment Plan

```json
{
  "disease": "Powdery Mildew",
  "disease_severity": "Medium - Requires Prompt Treatment",
  "recovery_time": "1-2 weeks with consistent treatment",
  
  "primary_pesticide": {
    "product": "Potassium bicarbonate fungicide (Primary) OR Neem oil",
    "details": {
      "dosage": "5 g per liter (bicarbonate) OR 3 ml per liter (neem oil)",
      "water_requirement": "300-400 liters per hectare",
      "application_method": "Foliar spray during late afternoon or early evening",
      "best_time": "Late afternoon (3-6 PM) or early morning (6-8 AM)",
      "frequency": "Every 5 to 7 days",
      "duration": "2 to 4 sprays based on disease progression",
      "safety": "Use a sticker-spreader if label permits; avoid spraying in full sunlight (can cause leaf burn)",
      "note": "Both products have low toxicity and can be used near harvest"
    }
  },
  
  "alternative_pesticides": [
    {
      "name": "Sulfur powder 80% WP",
      "dosage": "2-2.5 g per liter",
      "cost_indicator": "$",
      "effectiveness": "High",
      "note": "Classic preventive & curative agent"
    },
    {
      "name": "Trichoderma (Bio-fungicide)",
      "dosage": "As per product label (typically 1-2 ml per liter)",
      "cost_indicator": "$$",
      "effectiveness": "Medium",
      "note": "Biological agent, organic approved"
    },
    {
      "name": "Baking soda spray (DIY)",
      "dosage": "1 tablespoon per liter + 1 ml soap per liter",
      "cost_indicator": "$",
      "effectiveness": "Medium (early stages)",
      "note": "Eco-friendly home remedy"
    }
  ],
  
  "primary_fertilizer": {
    "product": "Low-nitrogen liquid fertilizer with potassium support",
    "primary_product": "Potassium Nitrate (KNO3) or Potassium Sulfate (SOP)",
    "details": {
      "dosage": "3-5 g per liter",
      "timing": "Apply 2-3 days after fungicide spray, once disease suppression begins",
      "application_method": "Foliar spray in early morning or late afternoon",
      "goal": "Avoid soft, disease-prone lush vegetative growth; strengthen plant tissues",
      "critical_note": "REDUCE/STOP nitrogen fertilization during treatment - high N promotes fungal susceptibility",
      "repeat": "Every 12-15 days for 2-3 applications"
    }
  },
  
  "alternative_fertilizers": [
    {
      "name": "Potassium Nitrate - KNO3",
      "dosage": "3-5 g per liter",
      "timing": "2-3 days after fungicide",
      "note": "Strengthens plant resistance"
    },
    {
      "name": "Calcium + Potassium combo",
      "dosage": "3 g calcium chloride + 2 g potassium sulfate per liter",
      "timing": "After disease suppression",
      "note": "Improves tissue resilience"
    }
  ],
  
  "equipment_needed": [
    "Knapsack or backpack sprayer",
    "Measuring spoon/scale for powders",
    "Protective gloves and mask",
    "Pruning shears",
    "Container for mixing solution",
    "Soft-bristled brush (for light removal)"
  ],
  
  "preventive_measures": [
    "Increase sunlight exposure - prune dense foliage",
    "Prune lower branches to improve air circulation",
    "Avoid excess nitrogen fertilization",
    "Maintain humidity between 40-60% if possible",
    "Provide adequate spacing between plants",
    "Remove infected leaves as soon as spotted"
  ],
  
  "step_by_step_treatment": [
    "Step 1: IDENTIFY - Look for white or grayish powder coating on leaves, starting on upper surface.",
    "Step 2: PRUNE - Remove leaves heavily covered (>60%) with powdery growth; also remove 3-4 lower leaves for better air circulation.",
    "Step 3: PREPARE SOLUTION - Method A: Mix 5 g potassium bicarbonate per liter of water, stir well. Method B: Mix 3 ml neem oil + 1 ml dish soap per liter water.",
    "Step 4: SAFETY - Put on gloves, mask, and protective clothing.",
    "Step 5: SPRAY - Apply in late afternoon when temperature begins to cool; cover all infected and nearby leaves thoroughly on both surfaces.",
    "Step 6: REPEAT - Spray every 5-7 days for a minimum of 2 cycles; increase frequency in high humidity (spray every 5 days).",
    "Step 7: PRUNE CANOPY - Increase sunlight penetration, maintain 6-8 inches spacing between leaves where possible.",
    "Step 8: FERTILIZE - After 2-3 days of disease control, apply potassium-rich fertilizer (KNO3 or SOP) at 3-5 g per liter foliar spray.",
    "Step 9: ADJUST NUTRITION - Completely stop or reduce nitrogen fertilizer application for 1-2 weeks to avoid promoting new susceptible growth.",
    "Step 10: MONITOR - Scout every 3-4 days; continue sprays until new emerging leaves are completely symptom-free for 7-10 days."
  ],
  
  "success_indicators": [
    "White powder coating gradually disappears",
    "Leaves begin to regain normal green color",
    "No new white patches appear on young leaves",
    "Leaf curling diminishes",
    "Plant vigor returns"
  ],
  
  "key_precautions": [
    "Do not apply sulfur and some oils within 2-week intervals",
    "Do not spray in direct sunlight (causes leaf burn)",
    "Reduce nitrogen fertilizer during treatment",
    "Ensure good spray coverage on leaf undersides - where fungus prefers to grow",
    "Stop preventive sprays once disease is completely controlled"
  ],
  
  "important_notes": [
    "Powdery mildew thrives in warm days (70-80°F) and cool nights with low humidity",
    "Unlike other fungi, it spreads in DRY conditions - no standing water needed",
    "Improve ventilation is as important as fungicide spray",
    "Early treatment is critical - highly visible white powder can spread rapidly"
  ]
}
```

---

## Using These Responses

Frontend developers can:

1. **Extract and display** primary pesticide recommendation with highlighted dosage
2. **Create tabs/buttons** for alternative pesticide options
3. **Show timeline** for step-by-step treatment in a scrollable format
4. **Display checklist** for equipment needed before starting treatment
5. **Highlight success indicators** to help farmers track recovery
6. **Create calendar** showing spray dates automatically calculated
7. **Show warnings** with key precautions prominently
8. **Calculate equipment cost** using the cost_indicator ($, $$, etc.)

Each response contains:
- **disease**: Disease name for header/title
- **disease_severity**: To highlight urgency level
- **recovery_time**: Clear expectation for farmer
- **primary_pesticide**: Main recommendation
- **alternative_pesticides**: 3 options (chemical, chemical, organic)
- **primary_fertilizer**: Main recovery nutrition
- **alternative_fertilizers**: 2 options
- **equipment_needed**: Shopping list
- **preventive_measures**: Before and after treatment
- **step_by_step_treatment**: 10-step procedural guide
- **success_indicators**: What to look for
- **key_precautions**: Safety and warnings
- **important_notes**: Disease-specific context

All information is farmer-friendly and actionable.
