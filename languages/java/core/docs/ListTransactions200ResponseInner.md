

# ListTransactions200ResponseInner

## oneOf schemas
* [TransactionListItem](TransactionListItem.md)
* [TransactionListPaymentMethodItem](TransactionListPaymentMethodItem.md)

## Example
```java
// Import classes:
import co.revaly.sdk.core.model.ListTransactions200ResponseInner;
import co.revaly.sdk.core.model.TransactionListItem;
import co.revaly.sdk.core.model.TransactionListPaymentMethodItem;

public class Example {
    public static void main(String[] args) {
        ListTransactions200ResponseInner exampleListTransactions200ResponseInner = new ListTransactions200ResponseInner();

        // create a new TransactionListItem
        TransactionListItem exampleTransactionListItem = new TransactionListItem();
        // set ListTransactions200ResponseInner to TransactionListItem
        exampleListTransactions200ResponseInner.setActualInstance(exampleTransactionListItem);
        // to get back the TransactionListItem set earlier
        TransactionListItem testTransactionListItem = (TransactionListItem) exampleListTransactions200ResponseInner.getActualInstance();

        // create a new TransactionListPaymentMethodItem
        TransactionListPaymentMethodItem exampleTransactionListPaymentMethodItem = new TransactionListPaymentMethodItem();
        // set ListTransactions200ResponseInner to TransactionListPaymentMethodItem
        exampleListTransactions200ResponseInner.setActualInstance(exampleTransactionListPaymentMethodItem);
        // to get back the TransactionListPaymentMethodItem set earlier
        TransactionListPaymentMethodItem testTransactionListPaymentMethodItem = (TransactionListPaymentMethodItem) exampleListTransactions200ResponseInner.getActualInstance();
    }
}
```


