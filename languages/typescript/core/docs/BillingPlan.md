
# BillingPlan

Billing plan frequency and type for the subscription or payment model.  Available billing plans: - **trial**: Free or limited introductory period (variable interval, days/weeks) - **weekly**: Billed every week (1 week interval) - **twicePerWeek**: Billed twice per week (3-4 days interval) - User is billed 2x per week - **biWeekly**: Billed every 2 weeks (different than twice per month) - **biMonthly**: Billed twice per month (2x per month) - **monthly**: Standard monthly billing (1 month interval) - Standard SaaS cadence - **quarterly**: Billed every 3 months - Often used for small business or agency plans - **semiAnnual**: Billed every 6 months - Common prepaid option - **annual**: Billed yearly (12 months interval) - Discounted yearly plan - **biennial**: Billed every 2 years (24 months) - Long-term or enterprise contracts - **triennial**: Billed every 3 years (36 months) - Multi-year hosting or enterprise terms - **usageBased**: Pay-as-you-go or metered billing - Billed per usage or seat count each cycle (varies) - **lifetime**: One-time payment with no renewal required - **custom**: Negotiated or legacy plans with custom terms (variable) - **other**: Fallback for undefined, experimental, or unspecified billing plans 

## Properties

Name | Type
------------ | -------------

## Example

```typescript
import type { BillingPlan } from ''

// TODO: Update the object below with actual values
const example = {
} satisfies BillingPlan

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BillingPlan
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


