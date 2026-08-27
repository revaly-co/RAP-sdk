

# GetTransactionById200Response

## anyOf schemas
* [TransactionGroupResponse](TransactionGroupResponse.md)
* [TransactionResponse](TransactionResponse.md)

## Example
```java
// Import classes:
import co.revaly.sdk.core.model.GetTransactionById200Response;
import co.revaly.sdk.core.model.TransactionGroupResponse;
import co.revaly.sdk.core.model.TransactionResponse;

public class Example {
    public static void main(String[] args) {
        GetTransactionById200Response exampleGetTransactionById200Response = new GetTransactionById200Response();

        // create a new TransactionGroupResponse
        TransactionGroupResponse exampleTransactionGroupResponse = new TransactionGroupResponse();
        // set GetTransactionById200Response to TransactionGroupResponse
        exampleGetTransactionById200Response.setActualInstance(exampleTransactionGroupResponse);
        // to get back the TransactionGroupResponse set earlier
        TransactionGroupResponse testTransactionGroupResponse = (TransactionGroupResponse) exampleGetTransactionById200Response.getActualInstance();

        // create a new TransactionResponse
        TransactionResponse exampleTransactionResponse = new TransactionResponse();
        // set GetTransactionById200Response to TransactionResponse
        exampleGetTransactionById200Response.setActualInstance(exampleTransactionResponse);
        // to get back the TransactionResponse set earlier
        TransactionResponse testTransactionResponse = (TransactionResponse) exampleGetTransactionById200Response.getActualInstance();
    }
}
```


