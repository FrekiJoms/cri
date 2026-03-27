# CODE NI ZAFRAAAAAAAAHHH!!!
- gi tabangan ni jomsss

## Unsa ni nga project?

Sa akong pag sabot simple ni siya nga Flask project nga naay:
- `admin`
- `user`

Sa user side, naa nay separate pages pero same ra gihapon ug sidebar:
- Dashboard
- Pricing Management
- Discount Management
- Settings
- Logout

Ang pinaka focus karon kay ang `Pricing Management`.

## Module nga natackle

**Module 1 and 2**
- Pricing Dashboard
- Discount Dashboard

Note:
- ang `Discount Management` placeholder pa lang sa pagkakaron
- ang main working part gyud now kay `Pricing Management`

## Unsa ang recent changes?

### 1. Gi separate ang user pages

Before, usa ra ka page ang user dashboard nga murag gi ilis-ilisan lang ang sulod.

Karon, separate na sila nga pages:
- `userdashboard.html`
- `pricingdashboard.html`
- `discountdashboard.html`
- `settingsdashboard.html`

Pero ang style sa sidebar kay same ra gihapon para dili libog tan-awon.

### 2. Naa nay complete sidebar sa user side

Ang sidebar karon naa nay:
- Dashboard
- Pricing Management
- Discount Management
- Settings
- Logout

Meaning:
- if mo click ka sa `Pricing Management`, mo adto ka sa pricing page
- if mo click ka sa `Discount Management`, mo adto ka sa placeholder page
- if mo click ka sa `Settings`, mo adto ka sa settings page

## Routes nga naa sa `app.py`

Ang [app.py](c:/Users/ranbing143/Documents/Projects/cri/app.py) simple ra gihapon ug style.

Important routes:
- `/`
- `/login`
- `/admindashboard`
- `/userdashboard`
- `/userdashboard/pricing`
- `/userdashboard/discount`
- `/userdashboard/settings`
- `/logout`

Ang importante nga function para sa user tabs kay:

```python
@app.route('/userdashboard/<section>')
def userdashboard_section(section):
```

Kana nga function maoy mo decide unsang page ang i-open depende sa section.

## Pricing Management karon

Ang pricing page karon makahimo na ug:
- set ug product base price
- update ug product price
- view sa price history

Simple ra iyang flow:
1. butang ka `Product ID`
2. butang ka `Price`
3. click `Save Price`

Kung bag-o pa nga product ID:
- himoon siya as new product

Kung existing na nga product ID:
- ma update ang iya price

Then:
- ma save pud ang old ug new price sa history

## Wala nay hardcoded products sa Python

Before:
- naa tay products nga hardcoded sa `app.py`

Karon:
- gitangtang na sila
- ang pricing data naa na sa browser gamit `localStorage`

Meaning ani:
- ang data dili na gikan sa Python
- ang data dili pud database
- ang data ma save sa browser mismo

So kung mag add ka ug products sa pricing page:
- makita gihapon na after refresh
- basta same browser/device ra

Kung laing browser or laing PC:
- dili na makita didto kay local ra siya

## Gi gamit ang localStorage

Sa [pricingdashboard.html](c:/Users/ranbing143/Documents/Projects/cri/templates/pricingdashboard.html), JavaScript na ang nag manage sa products.

Mao ni ang idea:

```javascript
localStorage.setItem(storageKey, JSON.stringify(products));
```

ug

```javascript
const savedProducts = localStorage.getItem(storageKey);
```

Kana maoy rason nganong ma remember sa browser ang imong products ug prices.

## Product ID field mas sayon na gamiton

Ang `Product ID` input gi improve pud.

Karon:
- if mo click ka sa field
- or mo type ka

mo gawas ang existing saved product IDs as suggestions.

Helpful ni siya kay:
- dili naka mag memorise sa tanan product IDs
- dali ra kaayo ka maka pili sa existing product
- human ana, ilisan na lang nimo ang price

## Scrollable na ang pricing table

Ang product list sa ubos sa pricing page kay scrollable na.

Before:
- kung daghan na kaayo ug products, taas kaayo ang whole page

Karon:
- ang `tbody` na mismo ang naay scroll
- dili na kaayo motaas ang whole page

Important CSS:

```css
tbody {
    display: block;
    max-height: 320px;
    overflow-y: auto;
}
```

## Discount Management

Ang `Discount Management` page naa na sa sidebar, pero placeholder pa lang siya.

Sa pagkakaron:
- title/header ra sa page
- same sidebar gihapon

Gi butang lang siya daan para kompleto na ang navigation.

## Settings page

Simple pa pud ang settings page.

Naa ra didto:
- account/user info
- role info

Basic page ra sa pagkakaron.

## Unsa pa ang wala mausab

Mga butang nga simple pa gihapon:
- basic pa ang login logic
- hardcoded pa ang users
- walay database
- walay full session system
- browser-local ra ang pricing data

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

## Files nga involved sa recent changes

- [app.py](c:/Users/ranbing143/Documents/Projects/cri/app.py)
- [templates/userdashboard.html](c:/Users/ranbing143/Documents/Projects/cri/templates/userdashboard.html)
- [templates/pricingdashboard.html](c:/Users/ranbing143/Documents/Projects/cri/templates/pricingdashboard.html)
- [templates/discountdashboard.html](c:/Users/ranbing143/Documents/Projects/cri/templates/discountdashboard.html)
- [templates/settingsdashboard.html](c:/Users/ranbing143/Documents/Projects/cri/templates/settingsdashboard.html)

## Quick test sa pricing

1. Login sa app.
2. Adto sa `Pricing Management`.
3. Butang ug product ID, example `101`.
4. Butang ug price, example `50`.
5. Click `Save Price`.
6. Baliki ang same product ID.
7. Ilisi ang price, example `75`.
8. Tan-awa sa ubos ang updated price ug history.

## Explanation sa code sa Pricing Tab

Ang [pricingdashboard.html](c:/Users/ranbing143/Documents/Projects/cri/templates/pricingdashboard.html) kay naay 3 ka main parts:
- HTML structure
- CSS styling
- JavaScript logic

## HTML structure

Ang HTML mao ang nag buhat sa layout sa page.

Naa siyay:
- sidebar sa left
- main content sa right
- form para sa `Product ID` ug `Price`
- table para sa product list ug price history

Important nga part:

```html
<form id="pricingForm">
```

Kini nga form ang gamiton para mag save or update ug product price.

Naa pud ni nga part:

```html
<tbody id="pricingTableBody"></tbody>
```

Meaning ani:
- empty siya sa sugod
- JavaScript ang mo butang sa sulod niya dynamically

## CSS styling

Ang CSS kay para sa design ug layout.

Examples:
- sidebar design
- card design
- form inputs
- table style

Important pud nga part ang scrollable table:

```css
tbody {
    display: block;
    max-height: 320px;
    overflow-y: auto;
}
```

Meaning ani:
- if daghan na ug products
- ang table body na lang ang mo scroll
- dili na motaas kaayo ang whole page

## JavaScript logic

Ang JavaScript mao gyud ang main brain sa pricing tab.

Kini siya ang nag:
- kuha sa input values
- save sa data
- update sa products
- render sa table
- save sa browser gamit `localStorage`

## Important variables

Naay important variables sa script:
- `storageKey`
- `pricingForm`
- `productIdInput`
- `priceInput`
- `pricingTableBody`
- `statusMessage`

Pasabot ana:
- `storageKey` mao ang name sa data sa localStorage
- `pricingForm` mao ang form
- `productIdInput` mao ang Product ID field
- `priceInput` mao ang Price field
- `pricingTableBody` mao ang sulod sa table
- `statusMessage` mao ang area para sa success/error message

## `getProducts()`

Kini nga function mo read sa saved products gikan sa browser:

```javascript
function getProducts() {
    const savedProducts = localStorage.getItem(storageKey);
    return savedProducts ? JSON.parse(savedProducts) : [];
}
```

Meaning:
- tan-awon niya if naay existing saved products
- if naa, i-convert niya balik into JavaScript array
- if wala, empty array lang

## `saveProducts(products)`

Kini nga function mo save sa products sa browser:

```javascript
function saveProducts(products) {
    localStorage.setItem(storageKey, JSON.stringify(products));
}
```

Meaning:
- i-convert ang products ngadto ug string
- then i-save sa `localStorage`

## `showMessage(message, type)`

Kini ang mo display ug message sa user.

Example:
- success message
- error message

So kung na save successfully, mo gawas ang green nga message.
Kung naay sayop, mo gawas ang red nga message.

## `formatPrice(price)`

Kini ang mo format sa price into 2 decimal places:

```javascript
function formatPrice(price) {
    return Number(price).toFixed(2);
}
```

Example:
- `50` mahimong `50.00`

## `renderProductOptions()`

Kini nga function kay para sa Product ID suggestions.

Meaning:
- kuhaon niya ang tanan saved products
- himoon silang options
- i-connect sa Product ID input pinaagi sa `datalist`

Mao ni ang reason nganong if mo click ka or mo type ka sa Product ID field:
- makita nimo ang existing product IDs

Helpful ni siya para:
- dali ra ka makapili sa existing product
- dali ra ka maka update ug price

## `renderProducts()`

Kini nga function mo display sa tanan products sa table.

Buhaton niya:
- kuhaon ang products gikan sa localStorage
- limpyohan ang old table rows
- if walay products, mo show ug `No products saved yet.`
- if naa, himoan niya ug rows ang kada product

Ang kada row naa:
- Product ID
- Base Price
- Price History

## Form submit logic

Kini nga part importante kaayo:

```javascript
pricingForm.addEventListener("submit", function (event) {
```

Meaning:
- if mo click ka sa `Save Price`
- JavaScript ang mo handle sa form
- dili siya mo submit back sa Python route

Mga step nga mahitabo:

1. kuhaon ang `Product ID`
2. kuhaon ang `Price`
3. i-check if naay empty field
4. i-check if ang price kay greater than `0`
5. kuhaon ang current products gikan sa localStorage
6. tan-awon if existing na ba ang Product ID

If existing na:
- update ang base price
- append ug bagong entry sa price history

If new pa:
- create new product object
- save first history entry

Then after ana:
- i-save balik sa localStorage
- i-refresh ang suggestions
- i-refresh ang table
- i-reset ang form

## Unsa gyud ang role sa localStorage?

Simple answer:

Ang `localStorage` mao ang temporary storage sa browser.

Meaning:
- if mag save ka ug product today
- naa gihapon siya after refresh
- pero browser-specific ra siya

So:
- same browser = makita gihapon
- laing browser = wala didto

## Simple summary sa pricing tab code

Sa pinaka simple nga explanation:

Ang pricing tab nag allow sa user nga mag input ug `Product ID` ug `Price`. Ang JavaScript maoy mo save sa data sa browser gamit `localStorage`. If existing na ang product ID, i-update niya ang price. If new pa, maghimo siya ug bagong product. Dayon i-display niya tanan sa table together with price history.
