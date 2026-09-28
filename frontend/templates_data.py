"""Template gallery for LexCraft AI.

Pre-filled example payloads per document type so users can start from a
realistic draft in one click instead of a blank form."""

TEMPLATES = {
    "Employment Contract": {
        "icon": "💼",
        "blurb": "Full-time hire agreement covering role, compensation and confidentiality.",
        "parties": "Jane Doe (Employee), TechNova Inc. (Employer)",
        "dates": "April 10, 2026",
        "terms": (
            "Role: Software Engineer reporting to the Engineering Manager;"
            "Annual compensation: INR 12,00,000 payable monthly;"
            "Working hours: 40 hours per week, Monday to Friday;"
            "Confidentiality must be maintained during and after employment;"
            "Either party may terminate with 30 days written notice"
        ),
    },
    "NDA (Non-Disclosure Agreement)": {
        "icon": "🔒",
        "blurb": "Mutual confidentiality agreement for client or partner discussions.",
        "parties": "Alex Kumar (Disclosing Party), Brightline Consulting (Receiving Party)",
        "dates": "March 1, 2026",
        "terms": (
            "Definition of confidential information includes business plans and code;"
            "Confidentiality must be maintained for 3 years from disclosure;"
            "Information may be shared only with approved team members;"
            "Breach entitles the disclosing party to seek injunctive relief"
        ),
    },
    "Lease Agreement": {
        "icon": "🏠",
        "blurb": "Residential lease with rent, deposit and maintenance clauses.",
        "parties": "Priya Nair (Tenant), Sunrise Properties (Landlord)",
        "dates": "June 1, 2026",
        "terms": (
            "Monthly rent: INR 18,000 payable by the 5th of each month;"
            "Security deposit: INR 54,000 refundable on vacating;"
            "Maintenance charges included in the rent;"
            "Either party may terminate with 2 months notice"
        ),
    },
    "Freelance Work Contract": {
        "icon": "🧑‍💻",
        "blurb": "Project contract for independent contractors and clients.",
        "parties": "Rahul Verma (Freelancer), Studio Kite (Client)",
        "dates": "February 20, 2026",
        "terms": (
            "Scope: design and delivery of a marketing website;"
            "Payment to be made within 30 days of invoice;"
            "The provider agrees to deliver work by the agreed deadline;"
            "Client receives full rights on final payment"
        ),
    },
    "Service Agreement": {
        "icon": "🤝",
        "blurb": "Ongoing service engagement with SLA and payment terms.",
        "parties": "GreenLeaf Services (Service Provider), Orbit Foods (Client)",
        "dates": "January 15, 2026",
        "terms": (
            "Services: monthly facility cleaning as per Annexure A;"
            "Service level: response within 24 hours of request;"
            "Payment to be made within 15 days of invoice;"
            "Either party may terminate with 15 days notice"
        ),
    },
    "General Agreement": {
        "icon": "📄",
        "blurb": "Flexible agreement skeleton for everyday arrangements.",
        "parties": "Meera Iyer (Party A), Quantum Labs (Party B)",
        "dates": "May 5, 2026",
        "terms": (
            "Purpose: collaboration on a pilot project;"
            "Each party bears its own costs;"
            "Disputes resolved by mutual discussion first;"
            "Either party may exit with 15 days notice"
        ),
    },
}
