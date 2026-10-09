"""
build_pdfs.py - Generate the personal-finance knowledge-base PDFs for this RAG project.

The assignment requires each student to supply their OWN documents. Rather than
use copyrighted material, these four short guides are original, plain-language
explainers written for this project. Run this once to (re)create the PDFs:

    pip install reportlab
    python data/build_pdfs.py

Output: four PDFs in the same data/ folder, which ingestion.py then indexes.
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

DATA_DIR = Path(__file__).parent

STYLES = getSampleStyleSheet()
TITLE = ParagraphStyle("DocTitle", parent=STYLES["Title"], fontSize=20, spaceAfter=14)
H2 = ParagraphStyle("H2", parent=STYLES["Heading2"], fontSize=13, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("Body", parent=STYLES["BodyText"], fontSize=11, leading=15, spaceAfter=6)

# Each doc = (filename, title, [ (heading|None, paragraph), ... ])
DOCS = [
    ("01_budgeting_and_saving.pdf", "Budgeting and Saving: A Beginner's Guide", [
        (None, "Budgeting is simply a plan for your money. A good budget tells every dollar where to go before the month begins, so spending becomes a deliberate choice rather than a surprise at the end of the month."),
        ("The 50/30/20 rule", "A popular starting framework is the 50/30/20 rule. You spend about 50% of your after-tax income on needs (housing, food, transport, utilities), 30% on wants (entertainment, dining out, hobbies), and put the remaining 20% toward savings and paying down debt. The percentages are a guide, not a law; adjust them to your situation, but keep the savings portion non-negotiable."),
        ("Zero-based budgeting", "Zero-based budgeting takes this further: income minus all assigned expenses should equal zero, meaning every dollar has a job, including money assigned to savings. This method makes overspending obvious because there is no 'unaccounted' money to hide in."),
        ("Building an emergency fund", "An emergency fund is cash set aside for genuine emergencies such as job loss, medical bills, or urgent home and car repairs. A common guideline is to save three to six months of essential expenses. Keep this money in an easily accessible savings account, not invested in volatile assets, because you may need it at short notice. Start small: even one month of expenses is a meaningful buffer that keeps a setback from becoming a debt spiral."),
        ("Sinking funds", "A sinking fund is money saved gradually for a known, irregular future cost such as annual insurance premiums, holidays, or car maintenance. By setting aside a small amount each month, large bills no longer wreck a single month's budget."),
        ("Tracking and reviewing", "Tracking expenses is the foundation of any budget. Categorise spending into groups such as groceries, transport, housing, and entertainment to see where money actually goes; small recurring subscriptions often add up to a surprising annual total. Review the budget regularly, especially when prices rise, because inflation erodes purchasing power and may require trimming wants or finding extra income."),
    ]),
    ("02_investing_basics.pdf", "Investing Basics and Long-Term Growth", [
        (None, "Investing means putting money to work so it can grow over time. Unlike a savings account, investments carry risk, but over long periods they have historically grown faster than inflation."),
        ("Compound interest", "Compound interest is the engine of long-term wealth. It is the process where the returns you earn themselves begin to earn returns. Because growth builds on previous growth, money invested early can outgrow much larger amounts invested later. This is why starting early, even with small contributions, is so powerful."),
        ("Diversification", "Diversification means spreading money across many different investments so that a poor result in one is offset by others. A diversified portfolio reduces risk without necessarily reducing expected long-term returns. The simple idea is to avoid putting all your eggs in one basket."),
        ("Index funds", "Index funds hold every stock in a market index, such as the S&P 500, at very low cost. Because they track the whole market rather than trying to pick winners, they tend to outperform most actively managed funds over long horizons once fees are considered. For most beginners, low-cost broad index funds are a sensible core holding."),
        ("Risk and return", "Risk and return are linked. Assets with higher potential returns, such as stocks, also swing more in value, while bonds and cash are steadier but grow slowly. Your mix of assets should reflect your time horizon and how much short-term loss you can tolerate without panic-selling."),
        ("Dollar-cost averaging", "Dollar-cost averaging means investing a fixed amount at regular intervals regardless of price. It removes the temptation to time the market: you automatically buy more units when prices are low and fewer when prices are high, smoothing out volatility."),
        ("Retirement accounts", "Tax-advantaged retirement accounts (such as a 401(k) or IRA in the United States, or the CPF in Singapore) encourage long-term saving. Contributions may be tax-deferred or tax-free on withdrawal, and any employer matching is effectively free money you should not leave on the table."),
    ]),
    ("03_banking_and_credit.pdf", "Banking, Credit, and Payments Explained", [
        (None, "Understanding how everyday banking products work helps you avoid unnecessary fees and interest and keep more of your money."),
        ("Account types", "A savings account holds money you do not need immediately and pays interest. A current or checking account is built for everyday transactions and usually pays little or no interest. Most people keep both, moving spare cash into savings to earn a return while keeping enough in the current account for bills."),
        ("How credit cards work", "Credit cards let you borrow up to a limit and repay later. If you pay the full statement balance by the due date, you usually pay no interest. Carrying a balance triggers high interest charges, and paying only the minimum can keep you in debt for years. Treat a credit card like a convenient way to pay, not as extra income."),
        ("Credit scores", "A credit score summarises how reliably you repay debt. Lenders use it to decide whether to approve loans and what interest rate to offer. On-time payments and keeping your balances low relative to your limits (low credit utilisation) raise your score; missed payments and defaults lower it."),
        ("Loan interest", "Loan interest can be simple or compound, and the rate may be fixed or variable. A fixed rate stays the same for the loan term and gives predictable payments. A variable rate moves with the market and can rise or fall, changing your monthly cost."),
        ("Digital payments", "Digital payments such as bank transfers, e-wallets, and QR-code systems (for example PayNow in Singapore) let you move money instantly without cash. They rely on secure authentication and on settlement networks between banks to confirm each transaction."),
        ("Deposit insurance", "Deposit insurance protects customers if a bank fails. Schemes such as the FDIC in the United States or the SDIC in Singapore guarantee deposits up to a set limit per account holder, which maintains confidence in the banking system."),
    ]),
    ("04_fraud_and_account_security.pdf", "Protecting Yourself from Fraud and Scams", [
        (None, "Financial fraud is common and constantly evolving. A few simple habits dramatically reduce your risk of losing money to criminals."),
        ("Phishing", "Phishing is a scam where attackers impersonate a trusted organisation in emails, texts, or calls to trick you into revealing passwords or card details. Warning signs include urgent threats, requests for sensitive information, misspelled web addresses, and links that do not match your bank's real website. When in doubt, do not click; instead, type the bank's address yourself or call the number on the back of your card."),
        ("Two-factor authentication", "Two-factor authentication (2FA) adds a second check beyond your password, such as a one-time code from an app or sent to your phone. Even if a criminal steals your password, they cannot log in without that second factor, so 2FA greatly reduces account takeover."),
        ("Strong, unique passwords", "Reusing one password across many sites means a single breach can compromise all of them. Use a long, unique password for each financial account, and a reputable password manager to store them. This is one of the highest-impact security habits."),
        ("Card skimming", "Card skimming uses hidden devices on ATMs or payment terminals to copy your card data. Cover the keypad when entering your PIN, check machines for loose or unusual attachments, and prefer contactless or chip transactions over magnetic-stripe swipes."),
        ("Identity theft", "Identity theft happens when someone uses your personal information to open accounts or make purchases in your name. Protect documents, shred old statements, and monitor your credit report so you can detect and limit damage early."),
        ("Investment scams", "Investment scams promise unusually high, guaranteed returns with little or no risk. Red flags include pressure to act fast, unlicensed sellers, and strategies that cannot be clearly explained. If an offer sounds too good to be true, it almost always is."),
    ]),
]


def build_pdf(filename: str, title: str, blocks):
    path = DATA_DIR / filename
    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    )
    flow = [Paragraph(title, TITLE), Spacer(1, 6)]
    for heading, text in blocks:
        if heading:
            flow.append(Paragraph(heading, H2))
        flow.append(Paragraph(text, BODY))
    doc.build(flow)
    print(f"Wrote {path.name}")


if __name__ == "__main__":
    for filename, title, blocks in DOCS:
        build_pdf(filename, title, blocks)
    print(f"Done. {len(DOCS)} PDFs created in {DATA_DIR}/")
