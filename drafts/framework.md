 # **Strategic Transparency Framework: Architecting a Data-Driven RTI Campaign for Bellandur Road Infrastructure**

## **1\. Executive Summary**

In the domain of civic governance, information asymmetry is the primary barrier to accountability. For a citizen-led initiative aiming to build a transparency portal for road infrastructure in Bellandur, Bengaluru, the challenge is not merely accessing documents but extracting structured, relational data from a bureaucratic system designed around paper trails and obfuscated hierarchies. This report outlines a comprehensive strategy to utilize the Right to Information (RTI) Act, 2005, not as a mechanism for grievance redressal, but as a rigorous data extraction protocol. The objective is to populate a relational database that maps road assets to contractor performance, budgetary outlays, and bureaucratic tenure, specifically within the jurisdiction of the Bruhat Bengaluru Mahanagara Palike (BBMP).

The focus on Bellandur (Ward 150 under the pre-2023 delimitation, now fragmented under the new draft notifications) presents a unique case study. It sits at the intersection of rapid urbanization, high revenue generation, and severe infrastructural deficits. To build a "usable and useful" web portal, one must bypass the superficial layers of governance—such as press releases or generic budget announcements—and access the "atomic units" of civic work: the Job Code, the Work Order (WO), the Measurement Book (MB) abstract, and the Defect Liability Period (DLP) register. These four elements form the metadata backbone of any effective monitoring platform.

This report establishes that a single, monolithic RTI application is strategically non-viable due to the bifurcated administrative structure of Bengaluru’s road network. Roads in Bellandur are not governed by a single entity; they are split between the Zonal Engineering Division (Ward Roads) and the Central Project Division (Arterial/Major Roads). Consequently, this framework proposes a "Split-Application Strategy," detailing the precise text, dropdown selections, and follow-up mechanisms for each jurisdictional silo. It further analyzes the impending restructuring of the BBMP into five separate municipal corporations under the Greater Bengaluru Authority (GBA), predicting how this will impact data continuity and providing future-proofing measures for the transparency portal.1

By systematically decoding the administrative vernacular—translating "repairs" into "Job Codes" and "guarantees" into "DLP Schedules"—this report provides the blueprint for transforming raw bureaucratic disclosures into actionable intelligence. The ultimate output is a portal that does not just display data but enforces accountability by algorithmically identifying roads that have failed within their warranty periods, thereby pinning financial liability on specific contractors and administrative liability on specific engineers.

## ---

**2\. Jurisdictional Anatomy of Bellandur: The Data Landscape**

To effectively file an RTI application, one must first understand the "Target Schema"—the internal organizational structure of the agency holding the data. Bellandur is not merely a geographic location; it is a complex administrative entity where multiple jurisdictions overlap. A failure to understand this leads to RTI applications being transferred endlessly between departments under Section 6(3) of the Act, resulting in delays and data fragmentation.

### **2.1 The Dichotomy of Road Governance**

In Bengaluru, the governance of road infrastructure is strictly siloed based on the *classification* of the road. This distinction is the most critical factor in drafting your RTI application because the Public Information Officer (PIO) for one category does not hold the records for the other.3

#### **2.1.1 Ward Roads (The Micro-Network)**

These constitute approximately 80% of the road network by length but a smaller fraction of the total budget. They include internal layout roads (e.g., Green Glen Layout, reliable internal roads in Bellandur village), cross streets, and connecting lanes between apartment complexes.

* **Custodian:** The Office of the Executive Engineer (Mahadevapura Division).  
* **Budget Head:** These works are funded under "Ward Works," "P-Code Grants," or specific "Mayor’s Grants."  
* **Data Characteristics:** High volume of small contracts (₹10 Lakh to ₹50 Lakh). These are the roads that directly affect "last-mile" connectivity for residents.  
* **RTI Target:** The PIO of the Mahadevapura Zonal Office. The data here is often localized and maintained in physical registers or decentralized computers at the Zonal office.5

#### **2.1.2 Arterial & Sub-Arterial Roads (The Major Network)**

These are the high-density corridors that carry the bulk of the city's traffic. In Bellandur, this includes critical arteries like the Sarjapur Main Road, portions of the Outer Ring Road (ORR), and the Varthur Main Road.

* **Custodian:** The Chief Engineer (Road Infrastructure \- Major Roads) or the Chief Engineer (Projects Central) stationed at the BBMP Head Office (N.R. Square).  
* **Budget Head:** Funded under "Major Roads," "TenderSURE," or "White-topping" grants.  
* **Data Characteristics:** Low volume of massive contracts (₹50 Crore+). These projects often involve specialized large-scale contractors and have different maintenance clauses (e.g., 5-10 years for white-topping).  
* **RTI Target:** The PIO of the Projects Division / Road Infrastructure at the Head Office. A Zonal PIO in Mahadevapura will *not* have the Measurement Books or Work Orders for these roads.4

#### **2.1.3 The Outer Ring Road (ORR) Anomaly**

The Outer Ring Road, which bisects Bellandur, presents a special jurisdictional case. Historically built by the Bangalore Development Authority (BDA), it was handed over to the BBMP for maintenance. However, owing to its strategic importance, it often falls under the purview of a specialized "Traffic Engineering Cell" (TEC) or the "OFC Ducts" division due to the high density of optical fiber cables. Recent reports indicate that the maintenance of key arterial roads forming boundaries between corporations is a subject of specific concern in the upcoming restructuring.6 For the purpose of the web portal, data regarding the ORR must be requested separately from the "Projects Central" division, as the local ward engineer typically has no jurisdiction over the ORR carriageway, only the service roads in some instances.

### **2.2 The "Job Code" as the Primary Key**

The single most important data point for your web portal is the **Job Code** (also known as the Work Code or P-Code). Without this, building a relational database is impossible.

* **Structure:** The Job Code is typically an alphanumeric string formatted as XXX-YY-NNNNNN.8  
  * XXX: Represents the Ward Number (e.g., 150 for Bellandur).  
  * YY: Represents the Financial Year (e.g., 18 for 2018-19).  
  * NNNNNN: A unique serial number for the work.  
* **Strategic Insight:** If the web portal indexes roads by "Road Name" (e.g., "7th Cross"), it will fail because names vary in records (e.g., "7th Cross, Green Glen" vs. "Road leading to Sobha Apartments"). Indexing by "Job Code" allows the portal to link multiple distinct contracts (e.g., Asphalting in 2019, Drain Repair in 2021, Footpath Relaying in 2023\) to a single geospatial entity. The RTI application must explicitly request the *decoding* of these Job Codes to map them to physical locations.

### **2.3 The Impact of "Greater Bengaluru Authority" Restructuring**

The governance landscape of Bengaluru is currently in flux due to the proposed **Greater Bengaluru Authority (GBA)** bill, which aims to split the BBMP into five distinct municipal corporations: Bengaluru East, West, North, South, and Central.1

* **Implication for Bellandur:** Bellandur, currently in the Mahadevapura Zone, is slated to become part of the **Bengaluru East Municipal Corporation**.11  
* **Data Continuity Risk:** When administrative boundaries shift, legacy data (paper files) often gets lost or becomes inaccessible during the transition.  
* **Strategic Urgency:** Filing the RTI *now* (in the 2025-26 period) is critical to secure the "baseline data" before the bifurcation is fully operational. The current Mahadevapura Zonal Office is the repository for the last decade of data. Once the split happens, finding records from 2018 or 2019 will become exponentially more difficult as files are moved to new Corporation headquarters.  
* **Zonal Mapping:** The current Mahadevapura Zone is likely to be the core of the new East Corporation. Therefore, the RTI targets identified in this report (Mahadevapura Zonal Office) will remain relevant as the immediate custodians, even if the higher-level reporting structure changes.12

## ---

**3\. The Bureaucratic Data Architecture**

To design the "schema" of your web portal, you must mirror the "schema" of the government's internal record-keeping. We are not asking for "documents"; we are asking for "fields" that exist in specific registers.

### **3.1 The Work Order Register (The Master Ledger)**

Every engineering division maintains a "Work Order Register." This is the master ledger of all sanctioned works.

* **Fields to Extract:**  
  * **Job Code:** The unique identifier.  
  * **Name of Work:** The official administrative description (e.g., "Improvements to roads and drains in Bellandur village").  
  * **Agency/Contractor Name:** The legal entity executing the work.  
  * **Work Order Amount:** The value of the contract.  
  * **Date of Commencement:** The start date.  
  * **Stipulated Date of Completion:** The deadline.

### **3.2 The Measurement Book (MB) (The Proof of Work)**

The Measurement Book is the "holy grail" of civil works. It is where the Assistant Engineer (AE) records the physical dimensions of the work done (length, width, depth of asphalt) to claim payment.

* **Relevance for Portal:** The MB contains the **names of the officials** who recorded and checked the work. This is the direct link to bureaucratic accountability.  
  * **Recording Officer:** Usually the Assistant Engineer (AE).  
  * **Check Measurement Officer:** Usually the Assistant Executive Engineer (AEE).  
  * **Superintending Officer:** The Executive Engineer (EE).  
* **RTI Strategy:** Requesting the entire MB for every road is voluminous and will be rejected. Instead, we request the **"MB Abstract"** or the "Final Bill Abstract," which summarizes the work and lists the signatories.

### **3.3 The Defect Liability Period (DLP) Register**

This is the most critical dataset for the "usability" of your portal.

* **Concept:** The DLP is the warranty period. For asphalt roads, it is typically **3 years**; for concrete roads, **5 years**; and for major white-topping, **10 years**.3  
* **Accountability Mechanism:** If a road develops a pothole during the DLP, the contractor must fix it at their own cost. If the BBMP spends taxpayer money to fix a road under DLP, it is a financial irregularity.  
* **Portal Feature:** Your website can color-code roads:  
  * **Green:** Under DLP (Citizen Action: Report to BBMP to force contractor repair).  
  * **Red:** DLP Expired (Citizen Action: Petition BBMP for maintenance).  
* **Data Availability:** The BBMP is mandated to maintain a "DLP Register" or a "Road History Register" that tracks these dates.

## ---

**4\. Strategic RTI Formulation: The "Split-Application" Approach**

A common mistake in RTI activism is filing a single "catch-all" application. If you file one application asking for "All roads in Bellandur and Outer Ring Road," the Mahadevapura PIO will deny having data for ORR (Major Roads) and may transfer the entire application, causing it to enter a bureaucratic limbo.

**The Strategy:** We will file **two separate online applications**.

1. **Application A (The "Ward" Application):** Targeted at the Mahadevapura Zonal Office. This captures 80% of the roads (internal layout roads, village roads). This is the high-yield, low-resistance application.  
2. **Application B (The "Major Roads" Application):** Targeted at the BBMP Head Office (Projects). This captures the high-profile arterial roads (ORR, Sarjapur Road).

Below is the precise text and configuration for **Application A**, which is the priority for a community-focused portal.

### **4.1 RTI Application A: Bellandur Ward Works (Internal Roads)**

**Filing Instructions:**

* **Portal:** rtionline.karnataka.gov.in  
* **Public Authority:** Select **"Bruhat Bengaluru Mahanagara Palike (Mahadevapura Zone) BBMP"**. (If this specific option is missing, select "Bruhat Bengaluru Mahanagara Palike (Office of the Commissioner)" and strictly add the "FORWARD TO" line at the top of the text).  
* **Payment:** ₹10 via Internet Banking/UPI.

**Text for "RTI Request" Field (Max 3000 chars):**

To: Public Information Officer (PIO),

Office of the Executive Engineer,

BBMP Mahadevapura Division,

Mahadevapura Zone, Bengaluru.

Subject: Request for "Road History," "Work Order," and "DLP" Data for Ward No. 150 (Bellandur) \- Period 2018-2025 \- For Public Transparency Portal.

Respected Sir/Madam,

Under the RTI Act 2005, I request the following structured data regarding Road Infrastructure Works (Capital & Maintenance) executed in Ward No. 150 (Bellandur) and its constituent areas (including Green Glen Layout, Kaikondrahalli, Kasavanahalli, Haralur, Junnasandra) for the financial years 2018-19 to 2024-25.

1. DATABASE OF EXECUTED WORKS:  
   Please provide a certified tabular list (Excel/CSV format requested) of ALL road works (Asphalting, Concreting, Pot-hole filling, Drain remodeling, Footpath) executed in the ward. For EACH work, provide:  
   a) Job Code / P-Code (e.g., 150-19-0000XX).  
   b) Name of Work (Administrative Sanction Description).  
   c) Name of the Agency/Contractor (Legal Entity Name).  
   d) Work Order (WO) Number & Date.  
   e) Work Order Amount (Sanctioned Cost).  
   f) Actual Completion Date (as per Measurement Book).  
   g) Defect Liability Period (DLP) Status: Specific Start Date and End Date of the DLP for each work.  
2. EXPENDITURE & ACCOUNTABILITY MAPPING:  
   For the works identified in Item 1:  
   a) Total Amount Paid to the contractor to date (Gross Bill Amount).  
   b) Designation & Name of the Officials (AE, AEE, and Executive Engineer) who were the "Check Measurement" officers responsible for certifying the quality of these specific works.  
   c) Copy of the "DLP Register" or "Road History Register" for this ward, showing the current liability status of all roads.  
3. CONTACT INFORMATION FOR PUBLIC GRIEVANCE:  
   Please provide the current official contact details (Name, Official Designation, Office Address, Official Mobile No, and Official Email ID) for:  
   a) The Executive Engineer (Mahadevapura Division).  
   b) The Assistant Executive Engineer (AEE) for Bellandur Sub-division.  
   c) The Assistant Revenue Officer (ARO) for Bellandur.  
4. FORMAT & SECTION 4 DISCLOSURE:  
   I request this data in digital format (CD/DVD/Email) to minimize paper use and facilitate data analysis for public interest, as mandated by Section 4(1)(b) of the RTI Act regarding computerization of records. If "Road History" is available on the BBMP "Road History 2.0" or "e-Aasthi" portal, please provide the specific URL and the list of available attributes.

Note: If any road (e.g., ORR, Sarjapur Main Road) falls under "Major Roads" or "Projects Central" jurisdiction, kindly provide the data available with your office (Ward Roads) and transfer only the specific relevant part of this application to the concerned PIO under Section 6(3). Do not transfer the entire application.

### **4.2 RTI Application B: Major Roads (Arterial Network)**

**Filing Instructions:**

* **Public Authority:** Select **"Bruhat Bengaluru Mahanagara Palike (Office of the Commissioner)"** or **"BBMP (Projects)"** if listed.  
* **Focus:** This application specifically targets the high-value projects that the Zonal office doesn't track.

**Text Modification:**

* Change the Subject to: "Request for Data on Arterial/Sub-Arterial Roads in Mahadevapura Zone (ORR, Sarjapur Road, Varthur Road)."  
* In the description, specify: "Works executed by the **Projects Division (Central)**, **Road Infrastructure**, or **Traffic Engineering Cell**."  
* Ask specifically for **"TenderSURE"** and **"White-topping"** package details, as these have distinct Job Codes and 5-10 year DLP clauses.

## ---

**5\. The Transparency Portal Blueprint: From Data to Usability**

The user's request emphasizes making the platform "actually usable and useful." This section translates the raw RTI data into a technical schema for the web application.

### **5.1 Database Schema (Relational Model)**

To build a robust portal, you need a relational database (SQL) that links assets to actors.

| Table Name | Primary Key | Key Fields (from RTI) | Purpose |
| :---- | :---- | :---- | :---- |
| **Roads** | road\_id | Road Name, Start Lat/Long, End Lat/Long, Surface Type, Width | The geospatial asset registry. |
| **Works** | job\_code | road\_id (FK), Description, Sanction Date, Cost, Contractor (FK) | The history of interventions on a road. |
| **Contractors** | contractor\_id | Legal Name, Address, Registration Class | To track performance across multiple wards. |
| **Officials** | official\_id | Name, Designation, Tenure Start, Tenure End | To map accountability to individuals over time. |
| **DLP\_Status** | dlp\_id | job\_code (FK), Start Date, End Date, Status (Active/Expired) | The core "Warranty Tracker" engine. |

### **5.2 The "DLP Algorithm" (The Core Utility)**

The most "useful" feature for a resident is to know *who* is responsible for a pothole. The portal should implement a simple logic:

1. **Input:** User selects a road segment (e.g., "7th Cross").  
2. **Query:** SELECT \* FROM Works WHERE road\_id \= '7th Cross' ORDER BY completion\_date DESC LIMIT 1\.  
3. **Check:** Is Current Date \< DLP End Date?  
4. **Output:**  
   * **IF YES:** "This road is under warranty by \[Contractor Name\] until. The BBMP cannot spend money to fix this. Click here to file a complaint demanding contractor action."  
   * **IF NO:** "This road is out of warranty. Maintenance is the responsibility of the BBMP AEE \[Name\]."

### **5.3 Integrating Contact Details**

The RTI request asks for "Official Contact Details." This is crucial because personal numbers change, but official designations remain.

* **Data Source:** The snippet 14 provides current names (e.g., **K.N. Ramesh, I.A.S.** as Zonal Commissioner, **Hemanth Sharan J** as Joint Commissioner).  
* **Portal Feature:** A dynamic "Who to Call" widget.  
  * *Constraint:* Do not hardcode names. Use the "Designation" as the anchor and allow for updates.  
  * *Historical View:* "In 2019, when this road failed, the Executive Engineer in charge was." This creates a permanent record of administrative tenure, discouraging negligence.

### **5.4 Usability Enhancements**

* **Geospatial Visualization:** The RTI response may not give coordinates. You will need to "crowdsource" the mapping or use OpenStreetMap (OSM) to link the "Road Names" from the RTI to actual map lines.  
* **Search by Contractor:** Allow users to see a "Portfolio" for a contractor. "Show me all roads built by 'M/s XYZ Constructions'." If they are all red (bad quality), the community has data to lobby against future tenders for that firm.  
* **Budget Per Kilometer:** Calculate the Work Order Amount / Road Length. This metric (e.g., ₹50 Lakhs/km vs ₹2 Crores/km) highlights potential inflation or gold-plating of estimates.

## ---

**6\. Operational Execution & Contingencies**

The RTI filing is just the first step. The response will likely be imperfect. This section details the operational handling of the government's response.

### **6.1 The "Data Not Available" Defense**

A common response from PIOs is: "The data is not available in the requested format (Excel). Please come to the office and inspect the files."

* **Counter-Strategy:** This is a tactic to deter analysis.  
* **Legal Rebuttal:** Cite **Section 4(1)(b)(vi)** of the RTI Act ("A statement of the categories of documents that are held by it or under its control"). The "Work Order Register" is a statutory document (Form PW-III). It *must* exist.  
* **Execution:** If forced to inspect, take a portable scanner or a high-quality camera app. Photograph the *entire* register for the relevant years. Then, use OCR (Optical Character Recognition) or volunteer crowdsourcing to digitize the handwritten entries into your Excel schema.

### **6.2 Handling Section 6(3) Transfers**

If the Mahadevapura PIO transfers the *entire* application to the Head Office because of the "Major Roads" clause:

* **Immediate Action:** File a **First Appeal** with the Appellate Authority (usually the Superintending Engineer or Chief Engineer of the Zone).  
* **Argument:** "The application specifically requested data for *Ward Roads* which are under the jurisdiction of the Mahadevapura Division. The PIO has erred in transferring the entire application instead of providing the available information and transferring only the remainder."

### **6.3 Verification of Data Existence**

The user query asks: "We have to obviously make sure that all of this data actually exists."

* **Confirmation:** Yes, the data exists legally.  
  * **Job Codes:** Every rupee spent by BBMP is tied to a Job Code in the IFMS (Integrated Financial Management System). It is impossible for a payment to be processed without it.8  
  * **Work Orders:** No contractor enters a site without a WO.  
  * **MB Abstracts:** No bill is passed without an MB recording.  
* **The Gap:** The "DLP Register" is often poorly maintained. If the PIO says "DLP Register not maintained," this is a *substantive admission of maladministration*. You can use this admission to file a complaint with the Lokayukta or the Technical Vigilance Cell (TVCC).

## ---

**7\. Future-Proofing: The GBA Transition**

The snippets indicate a massive restructuring of Bengaluru's governance into the **Greater Bengaluru Authority (GBA)** by late 2025/2026.1

### **7.1 The 5-Corporation Split**

Bellandur will likely move to the **Bengaluru East Corporation**.

* **Impact on Portal:** Your database must have a field for "Corporation Name" to allow for filtering.  
* **Data Migration:** As files move from the current centralized BBMP server to the new Corporations, links may break.  
* **Strategy:** Download and archive all "Road History" PDFs currently available on the BBMP website.15 These documents often disappear during website migrations. Your portal should serve as the *permanent archive* of these documents, independent of government servers.

### **7.2 Contact Details Flux**

During the transition, officials will be shuffled. The "Contact Details" you receive in the RTI response might be obsolete in 6 months.

* **Mitigation:** In the portal, implement a "Verified Date" tag next to phone numbers. Encourage users to "Report Incorrect Number," creating a crowdsourced directory maintenance system.

## ---

**8\. Conclusion**

Transparency in road infrastructure is not about accessing a single document; it is about reconstructing the chain of custody for public funds. By using the **Job Code** as the central thread, this framework connects the abstract notion of "governance" to the concrete reality of "contractor liability."

The split-application strategy outlined above—separating the granular Ward Works from the massive Major Projects—maximizes the probability of a high-quality response. By populating the proposed database schema with this RTI data, the resulting web portal will not just *show* information; it will *operationalize* it, arming the residents of Bellandur with the forensic evidence needed to demand the quality of infrastructure they have paid for. The impending GBA restructuring only heightens the urgency: the window to secure the historical data of the "BBMP era" is closing, and this data will be the baseline against which the new Corporations must be measured.

### **9\. Annexure: List of Relevant Authorities for Bellandur (2025-26)**

(Based on current data 14, subject to verification via RTI)

| Designation | Jurisdiction | Relevance |
| :---- | :---- | :---- |
| **Zonal Commissioner (Mahadevapura)** | Overall Zonal Admin | Review of First Appeals |
| **Chief Engineer (Mahadevapura)** | Technical Head (Zone) | Approves large ward works |
| **Executive Engineer (Mahadevapura Div)** | Ward Roads | **Primary RTI PIO** |
| **Chief Engineer (Projects Central)** | Major Roads (ORR) | **Secondary RTI PIO** |
| **Assistant Revenue Officer (Bellandur)** | Property Tax / Khata | Secondary contact for boundary issues |

This strategic framework provides the necessary depth, technical specification, and operational guidance to turn a general intent for transparency into a specific, executable, and high-impact digital platform.

#### **Works cited**

1. Bruhat Bengaluru Mahanagara Palike \- Wikipedia, accessed February 8, 2026, [https://en.wikipedia.org/wiki/Bruhat\_Bengaluru\_Mahanagara\_Palike](https://en.wikipedia.org/wiki/Bruhat_Bengaluru_Mahanagara_Palike)  
2. Greater Bengaluru Authority Corporations Delimitation 2025 \- Dataset \- CKAN, accessed February 8, 2026, [https://data.opencity.in/dataset/greater-bengaluru-authority-corporations-delimitation-2025](https://data.opencity.in/dataset/greater-bengaluru-authority-corporations-delimitation-2025)  
3. guidelines for construction and maintenance of city roads, accessed February 8, 2026, [https://data.opencity.in/dataset/b10ce2f1-5be5-44c4-8459-a08cf0a79c14/resource/6cf97bd1-5804-42e7-bac1-1456b7eeffb0/download/9fe52d23-d8ce-45c0-8119-108535737cde.pdf](https://data.opencity.in/dataset/b10ce2f1-5be5-44c4-8459-a08cf0a79c14/resource/6cf97bd1-5804-42e7-bac1-1456b7eeffb0/download/9fe52d23-d8ce-45c0-8119-108535737cde.pdf)  
4. BBMP Arterial and Sub Arterial Roads List \- Dataset \- CKAN, accessed February 8, 2026, [https://data.opencity.in/dataset/bbmp-arterial-and-sub-arterial-roads-list](https://data.opencity.in/dataset/bbmp-arterial-and-sub-arterial-roads-list)  
5. GBA \- Greater Bengaluru Authority, accessed February 8, 2026, [http://bbmp.gov.in/](http://bbmp.gov.in/)  
6. BBMP division: Concerns over maintenance of key roads forming boundaries between multiple corporations \- The Hindu, accessed February 8, 2026, [https://www.thehindu.com/news/cities/bangalore/5-city-corporations-concerns-over-maintenance-of-key-roads-forming-boundaries-between-multiple-corporations/article69839445.ece](https://www.thehindu.com/news/cities/bangalore/5-city-corporations-concerns-over-maintenance-of-key-roads-forming-boundaries-between-multiple-corporations/article69839445.ece)  
7. Outer Ring Road, Bengaluru \- Wikipedia, accessed February 8, 2026, [https://en.wikipedia.org/wiki/Outer\_Ring\_Road,\_Bengaluru](https://en.wikipedia.org/wiki/Outer_Ring_Road,_Bengaluru)  
8. BBMP JOB CODES CREATED BETWEEN 1ST APR AND 31ST AUG 2015 \- Janaagraha, accessed February 8, 2026, [https://www.janaagraha.org/files/BBMP-Job-Codes-2015-16.pdf](https://www.janaagraha.org/files/BBMP-Job-Codes-2015-16.pdf)  
9. BBMP Sagayapuram ward POW-2010-2011Engineering \- CIVIC Bangalore, accessed February 8, 2026, [https://civicspace.in/2019/10/15/bbmp-sagayapuram-ward-pow-2010-2011engineering/](https://civicspace.in/2019/10/15/bbmp-sagayapuram-ward-pow-2010-2011engineering/)  
10. End of BBMP era: Bengaluru restructured into 5 corporations under Greater Bengaluru Authority \- Hindustan Times, accessed February 8, 2026, [https://www.hindustantimes.com/cities/bengaluru-news/end-of-bbmp-era-bengaluru-restructured-into-5-corporations-under-greater-bengaluru-authority-101756789872922.html](https://www.hindustantimes.com/cities/bengaluru-news/end-of-bbmp-era-bengaluru-restructured-into-5-corporations-under-greater-bengaluru-authority-101756789872922.html)  
11. Greater Bangalore Authority to Include 5 New Corporations \- KOTS, accessed February 8, 2026, [https://www.kots.world/blog/greater-bangalore-authority-to-include-5-new-corporations](https://www.kots.world/blog/greater-bangalore-authority-to-include-5-new-corporations)  
12. Bengaluru governance reshaped with formation of GBA \- Bangalore Mirror, accessed February 8, 2026, [https://bangaloremirror.indiatimes.com/bangalore/civic/bengaluru-governance-reshaped-with-formation-of-gba/articleshow/123663053.cms](https://bangaloremirror.indiatimes.com/bangalore/civic/bengaluru-governance-reshaped-with-formation-of-gba/articleshow/123663053.cms)  
13. Defects liability period \- Construction Law Made Easy, accessed February 8, 2026, [https://constructionlawmadeeasy.com/construction-law/chapter-10/defects-liability-period/](https://constructionlawmadeeasy.com/construction-law/chapter-10/defects-liability-period/)  
14. BBMP Property Tax System, accessed February 8, 2026, [https://bbmptax.karnataka.gov.in/officialsdetails.aspx](https://bbmptax.karnataka.gov.in/officialsdetails.aspx)  
15. BBMP Road History \- Dataset \- CKAN, accessed February 8, 2026, [https://data.opencity.in/dataset/bbmp-road-history](https://data.opencity.in/dataset/bbmp-road-history)

