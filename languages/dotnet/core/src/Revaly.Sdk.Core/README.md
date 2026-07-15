# Created with Openapi Generator

<a id="cli"></a>
## Creating the library
Create a config.yaml file similar to what is below, then run the following powershell command to generate the library `java -jar "<path>/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar" generate -c config.yaml`

```yaml
generatorName: csharp
inputSpec: /spec/openapi.bundled.yaml
outputDir: out

# https://openapi-generator.tech/docs/generators/csharp
additionalProperties:
  packageGuid: '{3A0FA9A2-BE47-4D62-9DDB-C37D0A146A5B}'

# https://openapi-generator.tech/docs/integrations/#github-integration
# gitHost:
# gitUserId:
# gitRepoId:

# https://openapi-generator.tech/docs/globals
# globalProperties:

# https://openapi-generator.tech/docs/customization/#inline-schema-naming
# inlineSchemaOptions:

# https://openapi-generator.tech/docs/customization/#name-mapping
# modelNameMappings:
# nameMappings:

# https://openapi-generator.tech/docs/customization/#openapi-normalizer
# openapiNormalizer:

# templateDir: https://openapi-generator.tech/docs/templating/#modifying-templates

# releaseNote:
```

<a id="usage"></a>
## Using the library in your project

```cs
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Revaly.Sdk.Core.Api;
using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Model;
using Org.OpenAPITools.Extensions;

namespace YourProject
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var host = CreateHostBuilder(args).Build();
            var api = host.Services.GetRequiredService<INotifyApi>();
            INotifyRevalyApiResponse apiResponse = await api.NotifyRevalyAsync("todo");
            NotifyResponse? model = apiResponse.Ok();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) => Host.CreateDefaultBuilder(args)
          .ConfigureApi((context, services, options) =>
          {
              // The type of token here depends on the api security specifications
              // Available token types are ApiKeyToken, BasicToken, BearerToken, HttpSigningToken, and OAuthToken.
              BearerToken token = new("<your token>");
              options.AddTokens(token);

              // optionally choose the method the tokens will be provided with, default is RateLimitProvider
              options.UseProvider<RateLimitProvider<BearerToken>, BearerToken>();

              options.ConfigureJsonOptions((jsonOptions) =>
              {
                  // your custom converters if any
              });

              options.AddApiHttpClients(client =>
              {
                  // client configuration
              }, builder =>
              {
                  builder
                      .AddRetryPolicy(2)
                      .AddTimeoutPolicy(TimeSpan.FromSeconds(5))
                      .AddCircuitBreakerPolicy(10, TimeSpan.FromSeconds(30));
                      // add whatever middleware you prefer
                  }
              );
          });
    }
}
```
<a id="questions"></a>
## Questions

- What about HttpRequest failures and retries?
  Configure Polly in the IHttpClientBuilder
- How are tokens used?
  Tokens are provided by a TokenProvider class. The default is RateLimitProvider which will perform client side rate limiting.
  Other providers can be used with the UseProvider method.
- Does an HttpRequest throw an error when the server response is not Ok?
  It depends how you made the request. If the return type is ApiResponse<T> no error will be thrown, though the Content property will be null.
  StatusCode and ReasonPhrase will contain information about the error.
  If the return type is T, then it will throw. If the return type is TOrDefault, it will return null.
- How do I validate requests and process responses?
  Use the provided On and After partial methods in the api classes.

## Api Information
- appName: Revaly
- appVersion: 2.1.3
- appDescription: Payment processing API for transaction and payment method management.  ## API Versioning  RAP supports an explicit, selectable API version so you can build against a stable, pinned contract while existing integrations keep working unchanged.  - **How to select a version:** send the &#x60;X-Api-Version&#x60; request header   (e.g. &#x60;X-Api-Version: 2.0&#x60;). The version lives in the header — request   URLs do not change. - **Default when omitted:** requests without the header (or with an   unrecognised header name) bind to the **base version &#x60;2.0&#x60;**, which is the   current contract. Existing integrations therefore continue unchanged. - **Unsupported versions:** a header naming a version that does not exist   returns **HTTP 400** with a structured error listing the supported   versions — a request is never silently bound to a different contract.   This includes an **empty or whitespace value**: if the &#x60;X-Api-Version&#x60;   header is present, it must name a supported version. Only a fully   absent header binds to the default. - **Supported versions** are advertised via the &#x60;api-supported-versions&#x60;   header on every response from the versioned API endpoints (payments,   payment methods, transactions, notify). Currently: &#x60;2.0&#x60;, &#x60;2.1&#x60;. - **Which version to use:** new integrations should pin **&#x60;2.1&#x60;**. It is   behaviourally identical to &#x60;2.0&#x60; today, and it is where future contract   refinements will land — pinning it now means you never migrate the   header. &#x60;2.0&#x60; is the frozen launch contract and remains the binding for   requests that send no version header. 

## Build
This C# SDK is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project.

- SDK version: 0.0.0-dev
- Generator version: 7.23.0
- Build package: org.openapitools.codegen.languages.CSharpClientCodegen
