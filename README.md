# boycott-golden-source

Collating all boycott and alternatives data into a single, golden-source, version-controlled repository. This can be consumed by software products and services.

Sources:

- https://pastebin.com/raw/ks9GRE4L


## Model

Standardised data model for each company:

Example: 

```yaml

  # name: required, brand name
- name: "Brand"

  # website: optional, website of company, useful for alternatives to help users navigate to and shop from
  website:
  # image_url: optional, link to brand logo image
  image_url: |-
    https://1000logos.net/wp-content/uploads/2023/03/Whiskas-Logo-2003.png

  # categories/tags: optional, for grouping data, makes it easier to find alternatives
  categories: []

  # parents: required, list of parents, since one brand can have different parent companies in a different country/region
  parents:
    # name: required, parent company name
  - name: "Parent Company"
  	
    # location: required, list of locations where this is the parent company of the brand
    location: [global]

    # level: required, boycotting level, one of direct, alternative
    level: direct		
    
    # details: optional - boycotting details, relevant for boycott brand, can be empty for alternative
    #   reason: reason for boycotting (if applicable)
    #   source_url: evidence for why this brand/parent should be boycotted
    details:			
      reason: |-
        **Wilson Partnership**

        **Wilson** has partnered with **Delta Galil Industries**, Ltd. (DELT/Tel Aviv Stock Exchange), the global manufacturer and marketer of branded and private label apparel products for men, women, and children. **Delta Galil Industries** is an **Israeli** textile firm headquartered in **Tel Aviv**, with plants around the world.
      source_url: |-
        https://deltagalil.com/brands/licensed-brands/default.aspx
```


## TODO

- high level location to country codes? https://www.iban.com/country-codes
- update empty parents (manual?)
- script to 




