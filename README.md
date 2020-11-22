# Optimize LendingClub's Profit by Predicting Borrower's Repayment Capability

LendingClub (LC) is one of the biggest P2P Lending platform in America. Since 2007, they’ve been bringing borrowers and investors together, transforming the way people access credit. Over the last 10 years, they've helped millions of people take control of their debt, grow their small businesses, and invest for the future. As a Borrower, you could loan up to \$ 40,000. As an Investor (Lender), you could invest your money at the minimum amount, \$ 25.

Firstly, this dataset is from [Pierian Data](https://github.com/Pierian-Data) which contains loan amount, loan term, interest rate, installment, grade, home ownership, purpose of the loan, loan_status, and many more. Basically, this dataset is available from [their site](https://www.lendingclub.com/info/download-data.action) which anyone can scrape from there.

The standard loan period was 3 years (36 months) up to 5 years (60 months). Investors were able to search and browse the loan listings on LC website then select the loans that they wanted to invest based on the provided information about the borrower's like the amount of loan, loan grade, and loan purpose.

Investors made money from the interest on these loans, but LC made money by charging borrowers an origination fee and investors a service fee. But the truth about P2P lending activity is, investors still have risks. There are many risks but at least only 2 main risks which can't be avoided by investors:
1. Losing money due to bad debts (credit risk).
  > *We've got to the most "commonplace" reason for losing money on some loans: when your borrowers aren't good enough and can't pay all your money back. This is called "credit risk".* -- [4thway.co.uk](https://www.4thway.co.uk/guides/seven-key-peer-peer-lending-risks/)
2. Losses because you can't sell early (liquidity risk).
  > *The ability to sell your loans early - before your borrowers repay them naturally - is not a God-given right. P2P lending returns are stable because most lenders hold onto loans until they're repaid. If lending became like the stock market, where people dip in and out all the time, it would start leading to similarly wild price swings. In lending, that means swings in interest earned or returns made.* -- [4thway.co.uk](https://www.4thway.co.uk/guides/seven-key-peer-peer-lending-risks/)

If investors don't get their return of interest, technically LC can't charge service fee to investors, which means LC do not get money and profit from them.

## Problems
1. What are the characteristics of borrowers who stop repaying their loan?
2. How to optimize LendingClub's profit since LendingClub made money by charging borrowers and investors a fee? 

## Goals
1. Find out the main factors what make borrowers stop repaying their loan.
2. Make a Machine Learning Model to ensure LendingClub's profit especially from investors.

## Project Limitation
In this project, we will focus on the range of loan amount between \$ 25 until \$ 10,000. Because, borrowers who have loan amount above \$10,000 has many consideration to be picked. Right? The other reason that this limitation exists is to minimize unwanted errors of Machine Learning later. So, the rest of loan amount will be handled by LC's proffesionals.

## Table of Contents:
1. Preparation of Dataset
2. Explanation of Each Column
3. Handling Missing Value
4. Feature Extraction
5. Outliers
6. Exploratory Data Analysis
7. Feature Engineering
8. Base Model for Initial Evaluation
9. Data Preprocessing
10. Machine Learning Modelling
11. Machine Learning Optimization
12. The Best Model
13. Conclusions
14. Recommendations









# 13) Conclusions
1. **83.18 % borrowers are likely to complete their loan amount** rather than 16.82 % borrowers who has been valued as charged-off.
2. Notice that **borrowers who loan 60 months has higher interest rate** (15.7%) rather than 36 months (12.8%)
3. 33.04% borrowers are grade 'B', and 28.3% borrowers are grade 'C'. Both grade 'B' and 'C' combined into 61.34% alone. The least percentage of borrowers is grade 'G'. **This tells us that LendingClub is the healthy platform for investors**.
4. **High risk high return**. Basically, if investors want to get high return, just put it their money in to the lowest grade with 25.6% interest rate but in here, we know is too risky.
5. Don't get amazed too quick, by the number of borrowers, 'B3' is the highest borrowers who complete their loan with 10,941 borrowers, but **when it comes to proportion, the highest percentage of borrowers who complete their loan is 'A1'** with 97.21%, meanwhile the 'B3' has 87.93% only.
7. Borrowers who have average **revolving balance about $11,106 tend to be charged off borrowers in 60 months of loan term**.
8. **Individual applications are tend to have high charged-off rate** compare to joint application type (or with two co-borrowers).
9. **Educational purpose borrowers** who have 11.43 debt-to-income ratio (which is the lowest ratio) **are the only one purpose which fully paid their loan**, compare to other purposes.
6. Generally speaking, **the main characteristics of borrowers who stop repay their loans** are have: high interest rate, high loan amount, high installment, high debt-to-income ratio, low grade and low sub grade.
10. **Machine learning model which built with Random Forest algorithm has Precision score 0.90 of 1.0.** Using Precision from classification report because we only focus to minimize False Positive which the actual is charged-off but the model predicts fully paid rather than the actual is fully paid but the model predicts charged-off. This is nightmare for lenders/ investors because the worst scenario is all lenders' money would be gone in no time.

# 14) Recommendations
1. LendingClub could offer subscription services to lenders that will help them to choose borrowers wisely. Let's say educating them with the facts like "High risk isn't always high return, but high understanding leands to high return". Except if the lenders put their money into A grade borrowers, they don't need many informations.
2. Machine Learning model can be included in the subscription services which can help lenders easily to pick borrowers. Lenders only need to put the information of borrowers and then one 'click' away, they get the result of borrowers' repayment capability.
