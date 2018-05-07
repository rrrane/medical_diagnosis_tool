# Medical Diagnosis Tool
---
The medical diagnosis tool helps a doctor to ask specific questions to the patient based on the information provided by the patient.
It has three components:
1. Rule-Base
2. Working Memory
3. Inference Engine

**1. Rule-Base:** This contains the set of rules specific to the domain. For example:
- very-high-fever --> high-fever
- whooping-cough --> cough
- touching-poison-ivy --> rash
- high-fever ^ congestion --> flu
- !high-fever ^ rash --> poison-ivy
- cough ^ very-high-fever --> whooping-cough
- !high-fever ^ !cough ^ !rash --> healthy
- patient_1 has disease ^ disease is contagious ^ patient_1 contacts patient_2 --> patient_2 has disease
- person_1 is a doctor ^ person_1 says person_2 has a disease --> person_2 has a disease
- person_1 is a doctor ^ person_1 says person_2 is healthy --> person_2 is healthy

**2. Working Memory:** Working memory is a set of antecedents. For example:

- 'has-symptom fever Ed very-high' (Ed has very high fever)
- 'has-symptom cough Ed positive' (Ed has cough) 
- 'not has-touched Alice poison-ivy' (Alice hasn't touched poison-ivy)
- 'says Max Alice has-disease poison-ivy' (Max says Alice has poison-ivy)
- 'says Grace Don healthy' (Grace says Don is healthy)
- 'is-doctor Grace positive' (Grace is a doctor)
- 'is-contagious whooping-cough yes' (Whooping-cough is contagious)
- 'contacts Ed Alice' (Ed is in contact with Alice)

**3. Inference Engine:** Inference engine deduces everything that can be deduced from the rules and the working memory.
It runs either in (i) normal mode or in (ii) question mode.

***(i) Normal Mode:*** In this mode, inference engine substitutes contents of working memory in the rule premises and finds new inferences.
These inferences are then added to the working memory and the cycle is executed again and again until no new inference can be made any more.
The engine simply ignores the rules the values of who's one or more antecedents are not available.

***(ii) Question Mode:*** This mode works exactly like the Normal Mode except that it asks user the values of antecedents if they are not
available in the working memory even after deducing all possible inferences.
