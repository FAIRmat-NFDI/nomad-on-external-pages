# NOMAD Central Platform catalogue metadata

Agreed content supplied for the EOSC Finland Node catalogue, transcribed from the supplied form. Field names, requirements, guidance, and vocabulary options are retained alongside the supplied content. Vocabulary lists are form options and do not indicate selected values; no selections or missing values have been inferred.

M = Mandatory; O = Optional. Cardinalities and requirement labels are reproduced as supplied.

For catalogue links and maintenance instructions, see the [README](README.md).


## Catalogue metadata

| Field | Cardinality | Requirement | Guidance | Content / vocabulary options |
| --- | --- | --- | --- | --- |
| `PID` | `1` | M | (URL/URN) PID of the service | https://doi.org/10.17616/R32K89 |
| `short-name` | `0..1` | O | (text) Short version of the official name (in all languages) | NOMAD Central Platform |
| `name_en` | `1` | M | (text) Brief and descriptive name of the service in English | NOMAD Central Platform |
| `name_fi` | `1` | M | (text) Brief and descriptive name of the service in Finnish | NOMAD Central Platform |
| `link_to_service_en` | `1` | O (M for EOSC!) | (URL) Link to service webpage / GUI with information about the service  maintained by the service owner in English. (if not available use any language version) | NB! the service page should also contain all GDPR and how to obtain service details.<br><br>https://about.nomad-lab.eu/ |
| `link_to_service_fi` | `0..1` | O | (URL) Link to service webpage / GUI with information about the service  maintained by the service owner in Finnish. (if not available use any language version) | NB! the service page should also contain all GDPR and how to obtain service details.<br><br>https://about.nomad-lab.eu/ |
| `description_en` | `1` | M | (text) A generic description in fairly non-technical terms in English (max 1000 characters) | NOMAD Central Platform is a free web service that allows you to share your data or use comprehensive data provided by others. You can use NOMAD Central to organize, analyze, share, and publish your materials science data, as well as explore, download, and analyze the data of your colleagues. NOMAD is not only about sharing files, it is about sharing data and making them FAIR (Findable, Accessible, Interoperable, Reusable). All data in NOMAD are organized in well-defined structures described by a formal schema. When you publish a project, you can assign it a Digital Object Identifier (DOI) so others can cite it. |
| `description_fi` | `1` | M | (text) A generic description in fairly non-technical terms in Finnish (max 1000 characters) | NOMAD Central Platform on maksuton verkkopalvelu, jossa voit jakaa omaa dataasi ja hyödyntää muiden tarjoamia laajoja aineistoja. Voit järjestää, analysoida, jakaa ja julkaista materiaalitieteen tutkimusdataasi sekä tutkia, ladata ja analysoida kollegoidesi dataa. NOMADissa jaat tiedostojen lisäksi dataa FAIR-periaatteiden mukaisesti. Tämä tarkoittaa, että data on löydettävää, saavutettavaa, yhteentoimivaa ja uudelleenkäytettävää. Kaikki NOMADin data on järjestetty selkeästi määriteltyihin rakenteisiin, jotka on kuvattu muodollisella skeemalla. Kun julkaiset projektin, voit antaa sille pysyvän DOI-tunnisteen (Digital Object Identifier), jonka avulla muut voivat viitata siihen. |
| `tagline_en` | `0..1` | M | (text) Short catchphrase describing the service in English. (100 characters). | From research data to shared knowledge |
| `tagline_fi` | `1` | M | (text) Short catchphrase describing the service in Finnish. (100 characters). | Tutkimusdatasta yhteiseksi tiedoksi |
| `Logo` | `0..1` | O | URL of the service's logo  -scalable vector graphic format (SVG) recommended, otherwise 120 pixels high. | https://about.nomad-lab.eu/assets/nomad.svg |
| `research_domain` | `1 (1..N)` | O (M for EOSC!) | (vocabulary) Research domain (not currently visible in eosc.fi service catalogue user interface, but probably will be later & needed in the API) | Natural Sciences: Biological Sciences; Chemical Sciences; Computer & Information Sciences; Earth & Related Environmental Sciences; Mathematics; Other Natural Sciences; Physical Sciences|
| `service_type` | `1 (1..N)` | M | 'category'  (EOSC data model) | Publishing & Discovery<br>Data Management & Curation<br>Data Processing & Analysis<br>Storage Services<br>Science Gateways<br><br>**If necessary, mapping will be made to CSC: purpose_of_the_service_en(AVOTT)**<br>- Compute & Analyze / Prossoi & analysoi dataa<br>- Store & share during project / Säilytä ja jaa dataa projektin aikana<br> - Publish & preserve data / Julkaise & säilytä pitkäaikaisesti dataa<br> -Discover & reuse / Etsi & uudelleenkäytä |
| `geographicalAvailabilities` | `1` | M | A local EOSC FI field used to inform about access | This field is used to filter services shown (Show me accessible services, if...). Current options 08/2026):<br><br>fi_affiliated (I'm a researcher in a Finnish organization)    tiukin rajaus<br><br>fi_invited    (I'm a researcher in a non-Finnish organization and I've been invited to a CSC project)    toiseksi tiukin rajaus<br><br>eosc (I'm a researcher in a non-Finnish organization) kattaa kaikki palvelut (mahdollista federoida myös muihin noodeihin, jos erikseen sovitaan) |
| `target_user (EEN data model)` | `1..N` | M | (vocabulary) List of target users for the service | - Research Organisations, including: Research Infrastructure Managers and Research Managers<br><br>- Research Networks, including: Research Communities <br><br> - Researchers, including: Research Groups and Research Projects<br><br>- Students|
| `target_customer` | `1..N` | M | vocabulary | - researcher - tutkija<br><br>- teacher - opetushenkilöstö<br><br>- student - opiskelija<br><br>- industry user - yrityskäyttäjä |
| `languageAvailabilities` | `1..N` | (M for EOSC!) | (vocabulary) List of language availabilities of the service (ISO 639-1 Code) | en (English)|
| `helpdeskEmail` | `0..1` | (O for EOSC) | (email) Email address for the service's helpdesk. | support@nomad-lab.eu |
| `securityContactEmail` | `0..1` | (O for EOSC) | (email) Email address for security contact. | support@nomad-lab.eu |
| `trl` | `1` | (M for EOSC!) | (vocabulary)Technology Readiness Level (trl-9 by default) | trl-9 - actual system proven in operational environment |
| `end_user_guidance_in_english` | `0..1` | O | (URL) Link to public user guide in English. | https://docs.nomad-lab.eu |
| `end_user_guidance_in_finnish` | `0..1` | O | (URL) Link to public user guide in Finnish. |  |
| `tou_en` | `0..1` | O | (URL) Link to Terms of Use in English. | https://about.nomad-lab.eu/terms.html |
| `tou_fi` | `0..1` | O | (URL) Link to Terms of Use in Finnish. |  |
| `privacy_en` | `0..1` | O | (URL) Link to Privacy Statement in English. | https://about.nomad-lab.eu/privacy.html |
| `privacy_fi` | `0..1` | O | (URL) Link to Privacy Statement in Finnish. |  |
| `order_type` | `1` | M (EOSC) | (vocabulary) | Open Access: No ordering procedure necessary to access the resource but requires user authentication.|
| `target_segment` | `1..N` | M | (vocabulary) Label describing the customer segment. |- Education - Koulutus<br> - Research - Tutkimus|
| `resource_provider (National data model)` | `1` | M | (text) | Name of the organization<br><br>Humboldt-Universität zu Berlin (https://ror.org/01hcx6992) |
| `requirements_en` | `0..1` | O | (text max 500 char) Explain technical requirements or details (especially needed skills or tools) for the use of the service. Also, mention possible other important technical features which can be showstoppers for the user or that they need to take into account. (in English) | Use a web browser to explore and download public data. A free NOMAD account is required to upload, share, or publish your own data. To use NOMAD’s automatic data extraction, upload files in a supported format. Python skills are useful for working with the API or writing your own analysis notebooks. |
| `requirements_fi` | `0..1` | O | (text max 500 char) Explain technical requirements or details (especially needed skills or tools) for the use of the service. Also, mention possible other important technical features which can be showstoppers for the user or that they need to take into account. (in Finnish) | Voit selata ja ladata julkisia aineistoja verkkoselaimella. Omien aineistojen lataaminen palveluun, jakaminen ja julkaiseminen edellyttävät maksutonta NOMAD-käyttäjätiliä. Automaattinen tietojen poiminta edellyttää, että tiedostot ovat tuetussa muodossa. Python-osaamisesta on hyötyä, jos käytät ohjelmointirajapintaa (API) tai laadit omia laskentamuistikirjoja |
| `training_en` | `0..1` | O | (URL) Tutorials and training materials in English. | https://docs.nomad-lab.eu/tutorial/overview.html |
| `training_fi` | `0..1` | O | (URL) Tutorials and training materials in Finnish. |  |
| `pricing_en` | `0..1` | O | (URL) Link to Pricing policy in English |  |
| `pricing_fi` | `0..1` | O | (URL) Link to Pricing policy in Finnish |  |
| `sla_en` | `0..1` | O | (URL) Link to public Service Level Agreement in English. |  |
| `sla_fi` | `0..1` | O | (URL)  Link to public Service Level Agreement in Finnish. |  |
| `obtain_fi` | `0..1` | O | (text max 500 char) How to obtain the service - What the end user needs to do to start using the service. In Finnish. | Avaa https://nomad-lab.eu verkkoselaimessasi. Voit selata ja ladata julkisia aineistoja ilman kirjautumista. Jos haluat ladata omia aineistojasi palveluun, jakaa niitä tai julkaista niitä, luo maksuton NOMAD-käyttäjätili tai kirjaudu Helmholtz AAI kautta. |
| `obtain_en` | `0..1` | O | (text max 500 char) How to obtain the service - What the end user needs to do to start using the service. In English. | Open https://nomad-lab.eu in your web browser. You can browse and download public datasets without signing in. To upload, share, or publish your own data, create a free NOMAD account or sign in through Helmholtz AAI. |
| `datatag_min` | `0..1` | O | Minimum protection level | Open access|
| `datatag_max` | `0..1` | O | Maximum protection level | Restricted and controlled access|

