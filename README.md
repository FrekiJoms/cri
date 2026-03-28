# CODE NI ZAFRAAAAAAAAHHH!!!
- gi tabangan ni jomsss

## PREVIEW
<img width="960" height="474" alt="image" src="https://github.com/user-attachments/assets/4c0876c7-2db0-410d-858c-05b2c9d0c0b1" />

## Unsa ni?

Simple ni nga Flask project nga naay:
- `admin`
- `user`

Sa user side, naa nay sidebar with:
- Dashboard
- Pricing Management
- Discount Management
- Settings
- Logout

## Module nga natackle

- Module 1: Pricing Management
- Module 2: Features

Note:
- ang `Pricing Management` ang pinaka working feature karon
- ang `Discount Management` placeholder pa lang

## Unsa ang latest changes?

- gi separate ang user pages into:
  - `userdashboard.html`
  - `pricingdashboard.html`
  - `discountdashboard.html`
  - `settingsdashboard.html`
- same ra gihapon ug sidebar ang user pages
- gitangtang ang hardcoded products sa Python
- gi balhin ang pricing data ngadto sa browser gamit `localStorage`
- ang pricing table kay scrollable na
- ang `Product ID` field mo suggest na ug existing saved products

## Routes sa `app.py`

Important routes:
- `/login`
- `/admindashboard`
- `/userdashboard`
- `/userdashboard/pricing`
- `/userdashboard/discount`
- `/userdashboard/settings`
- `/logout`

## Unsaon pag work sa Pricing Management?

Sa pricing page pwede ka:
- mo input ug `Product ID`
- mo input ug `Price`
- mo click ug `Save Price`

Behavior:
- kung new ang `Product ID`, mag create ug new product
- kung existing na ang `Product ID`, i-update ang price
- every update ma save sa `Price History`

## Asa gi save ang products?

Sa browser na mismo gamit `localStorage`.

Meaning:
- ma retain gihapon after refresh
- pero browser-only ra siya
- if laing browser or laing PC, dili makita didto

## Simple explanation sa pricing code

Ang [pricingdashboard.html](templates/pricingdashboard.html) kay naay 3 ka parts:

- HTML
  - mao ang layout sa page, form, ug table
- CSS
  - mao ang style sa sidebar, cards, ug scrollable table
- JavaScript
  - mao ang nag save, update, ug display sa products

Important JavaScript functions:
- `getProducts()`
  - mo kuha sa saved products gikan sa `localStorage`
- `saveProducts(products)`
  - mo save sa products balik sa `localStorage`
- `renderProductOptions()`
  - mo show ug existing product IDs as suggestions
- `renderProducts()`
  - mo display sa products ug price history sa table

## Discount Management

Naa na siya sa sidebar pero placeholder pa lang sa pagkakaron.

## Unsaon pag run

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/login
```

## Test accounts

Admin:
- username: `gwapo@bisu.edu.ph`
- password: `admin123`

User:
- username: `pangit@bisu.edu.ph`
- password: `user123`

## Quick test sa pricing

1. Login sa app.
2. Adto sa `Pricing Management`.
3. Butang ug product ID, example `101`.
4. Butang ug price, example `50`.
5. Click `Save Price`.
6. Baliki ang same product ID.
7. Ilisi ang price, example `75`.
8. Tan-awa sa ubos ang updated price ug history.

## Code explanation
basaha ra diri para sa complete explanation sa code:

- [code_explaination.md](code_explaination.md)
