

# GetTransactionByMerchantTransactionId200Response

## anyOf schemas
* [PendingTransactionResponse](PendingTransactionResponse.md)
* [TransactionGroupResponse](TransactionGroupResponse.md)
* [TransactionResponse](TransactionResponse.md)

## Example
```java
// Import classes:
import co.revaly.sdk.core.model.GetTransactionByMerchantTransactionId200Response;
import co.revaly.sdk.core.model.PendingTransactionResponse;
import co.revaly.sdk.core.model.TransactionGroupResponse;
import co.revaly.sdk.core.model.TransactionResponse;

public class Example {
    public static void main(String[] args) {
        GetTransactionByMerchantTransactionId200Response exampleGetTransactionByMerchantTransactionId200Response = new GetTransactionByMerchantTransactionId200Response();

        // create a new PendingTransactionResponse
        PendingTransactionResponse examplePendingTransactionResponse = new PendingTransactionResponse();
        // set GetTransactionByMerchantTransactionId200Response to PendingTransactionResponse
        exampleGetTransactionByMerchantTransactionId200Response.setActualInstance(examplePendingTransactionResponse);
        // to get back the PendingTransactionResponse set earlier
        PendingTransactionResponse testPendingTransactionResponse = (PendingTransactionResponse) exampleGetTransactionByMerchantTransactionId200Response.getActualInstance();

        // create a new TransactionGroupResponse
        TransactionGroupResponse exampleTransactionGroupResponse = new TransactionGroupResponse();
        // set GetTransactionByMerchantTransactionId200Response to TransactionGroupResponse
        exampleGetTransactionByMerchantTransactionId200Response.setActualInstance(exampleTransactionGroupResponse);
        // to get back the TransactionGroupResponse set earlier
        TransactionGroupResponse testTransactionGroupResponse = (TransactionGroupResponse) exampleGetTransactionByMerchantTransactionId200Response.getActualInstance();

        // create a new TransactionResponse
        TransactionResponse exampleTransactionResponse = new TransactionResponse();
        // set GetTransactionByMerchantTransactionId200Response to TransactionResponse
        exampleGetTransactionByMerchantTransactionId200Response.setActualInstance(exampleTransactionResponse);
        // to get back the TransactionResponse set earlier
        TransactionResponse testTransactionResponse = (TransactionResponse) exampleGetTransactionByMerchantTransactionId200Response.getActualInstance();
    }
}
```


