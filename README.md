# Node sharer v0.2.1

Easily share procedural materials and shader node setups as text!

![NodeSharer](./img/ns_header1_crop.png)

![showcase](https://thumbs.gfycat.com/LimpingUnequaledChameleon-size_restricted.gif)

[Watch it in high quality](https://giant.gfycat.com/LimpingUnequaledChameleon.webm)

## Installation
1. Download the zip-file from the green "Code" button near the top of the page or by clicking [here](https://github.com/wildiness/NodeSharer/archive/master.zip).
2. In Blender, go to Edit > Preferences > Add-ons
3. Choose "Install..." and select the just downloaded zip-file.
4. Node sharer should appear in the list. Check the checkbox to activate it.
5. Copy the text string below then, in Blender, go to the shading tab, in the shader editor press "Node" then scroll to the top of the list and select Paste material!

NS0B2900!eNqtVk1vozAQ/SuVz06EDeSDW7NNo0hJdtVuV12tKuQEJ7FEIAKT7ariv3dsTEnBaffQAwLPjMdv3jwGXlDCDhwFSPJcUoSR/HdUywOTPBMsBkuSRjxHwQtaGtvV90IeC6lM6zgUkclwv2cRz1YQXfmXTQqRwFrnoCj44/QdbK6nEpx5yDZSnHiYmrwyKzhGcbqBYNd3ses4T7gG2kYBkFm247ANXS8WCBL+SrM0ScXVT/4si4z3Hce/jBWCTDxkikQuWbJREdOHb4v5zfR6BeYtZyoRWG/pu2qcVjUYERSoharTV3cXBUTdPWX3MfL1uqyr6w2JgwkhTXk28BhVzNRnQiuKfJexEz8LG6KAlqUODaOTidRYyHuUBintYHdNvMaqMJ4qLGEkDjzJRZoAAOTeKI5nGYsET+QZAPIhyfUGKGZnHkOjtcV8Nb2++5DYhrAxGeEe8fyGMSuUd5RpZFZV+B3GLExVPVWRFtoHH1Zdb/h/1Xj9oe6E36e6E25/rFVDlX9g4oYtFRF4Q3DPJR7kOpgjO107cxnibydL1LxXttq6yrPSSPEFRXo2RWomxfNl4sB5N5vA4euYJ1GNdjl/bNOoX6m2vMmbvEllgUJGb56GNJdQTB33bLIApm7BPzKRbMQx5tHV5P7mFg79XDMQUOQ8ZPFxz1CwZXHOK8smZoejsZSXSPtSPdVTaNQnWk9aR5/pyXMp7g1GX6umoW2OKRk4VpFglO/Tv6Gs9lcfBTB22nGJrUkebZtgM9wzsS4kFKHGxuzRwqISSnWRNpNGThQuUk1LS7xn4n0jzjOG9Xpk1uN6Nr8NaVLLmdaWah678OSp/njK6dfOOjEZWuVPRubDQ8YdddCuYCi5NHAHrc9vm39LT9u/Cbq/ebHOi2zLNjw8cLlPI8g1ebhbTH+jsixfAao5cd4=

Check out [NodeShare.io](https://nodeshare.io/) by @nodeshareio, a website for sharing materials with Node Sharer!

Join the [Discord](https://discord.gg/c9fZKRb) if you have comments, or want to share materials with people!

## Using Node Sharer
Node sharer has two commands. 
* Copy material as text string
* Paste material from text string in clipboard

These commands are found under the "Node" button in the Shader editor. In the standard "Shading" tab
you will have to scroll to the top of the list.

#### Copy material
This command saves the currently active material in the Shader editor 
to the clipboard as a Node Sharer text string. Take note of the length
of this text string in the Blender info pop-up.

#### Paste material
Save your file before pasting! This command creates a new material from the Node Sharer text string saved in
the clipboard. Take note of the material name in the Blender info pop-up.
The material can then be selected in the Shader editor material selector.

![Menu location](./img/node_menu.png)

##### The text strings
The first 8-10 characters in an Node Sharer text string always follow the following format:
NS(version number)B(Blender version number) ! Base64 text string.
Example:
```NS0B2900!Base64...```

Node sharer text strings are JSON representations of materials, compressed with zlib
and then converted to base64. This way of sharing data is taken directly from the game Factorio. 
In which you can share blueprints of machines and assembly lines as text strings. 

### Support/help and bug reports
Creat a ticket here on Github or join the [Discord](https://discord.gg/UTBGCCv). But please check the list below first, 
It might be a known issue.

### Limitations and know bugs
* This is a Beta release, be careful and save your project before using the Node Sharer commands

* The following nodes are not supported at the moment, they can be copied and pasted but won't retain their settings:
    - Group input names and min/max values are not supported yet.
    - Script
    - Frame. The frame will not keep its size. And if nodes are parented(=placed inside) to the frame, 
    the pasted location will be wrong.

* Pasting materials with groups and especially nested groups can cause a crash to desktop. 
Avoid copying materials with groups for now. And only paste materials in a **SAVED** blend file.

* Nodes that use a file browser or object/UV map/Vertex group selector will not have the file path/object sent with Node Sharer, 
and so the pasted nodes will not have the correct files/object selected.

* The Node Sharer commands will appear in all node editors, including those from
other add-ons. However, the command will most likely not work with these custom nodes.

* If you use Blender in a language other than english and/or name nodes with non standard characters,
that could cause problems, maybe.
 
* Node values are rounded to 5 decimal places to save space. Location values are rounded to integers.

### Contributing
Share it with your friends! The usability of this add-on increases exponentially with the amount of users.

Pull request will be accepted(if I can figure out how to do it), but no PEP8ifying.
Create an issue first, to go along side the PR.

My goal with this add-on is to show the Blender Devs that easy sharing of nodes is something Blender needs to have built in.
And I hope something similar to this will be implemented in Blender so I don't have to maintain this.

### More materials
Here are 3 other materials you can try pasting:

```
NS0B2900!eNrNWV1vozgU/SuVnwnytyFvyfRDlZLMqpOuZjUaRTTQFimBCEhnVlX++9pgJhQMpVqa9iEiti/28fG519fmGUTeNgBjkAVpRoAFsn93qrj1siAJvY2siWI/SMH4Gcx13dnXfbbbZ6rqbrMKfd3Dt0fPD5KFtC7a58cuwkiW8z4wGP+ANrT07+dBNqYrb52FT8Eq1v1myT6wwCZeS2PCiEUg/GmVQOsoJGQveQjka2AymwHZ4Tz83Y5NNt5cTeVbd5sg8ld6uvPr7y9gQjCGNrMAyuEighi31NNxXUs1IFshKibDyskQiHnecijBj4jAFnJZBb3EZoFiouVIz+CvJIzW4W4T+GfTb+eXcvDDIbda+U/aqMpaydw+DVbeZvfogfG9t0mDoma98bY7XSON/o6TOIrDs2XwO9snQTsz0kDbSoR+mGZetFYWF7dfZtfnF5OFrL4PvKITcInqhL1Y15w6VVAkMfUkYIzUk2pqWV4+UuVyxxohhxy5qiNv8jbfpw+J9xQcJ8caxOUgkIFAqyHGHCT8A1KBeyowrPxwG0RpGEdycEDOtcxsCNEppQYpp9jSkqOE1uWGoMMsTMkLveUgDdwpL0HvprNuaj5Ya4g7SIqN8FaxtZFWE1wxy1OKzgigg+byhf4McpvnmIjGhNWT6SfXdqLOKEPUIlTIrrZ6xAb8SpP2hcvpHBylapqaUbfFpKGJ9YNRifjTKhEzh0ol8k4l4n5KxB8Q/siw4Q9C7pQBDjmCOI2dlgokHAUXUkFr4Q8L7FgY4nr4I60ywu8cAsmnFR4hWAlPdAqP9BMe+QDh4ZPuuzLglGkeq++5riNFhxqiw12xa0DRGdaDDbwjMNvJlwjbbv8dAUPCrJHj4GG3BGagtSlcBdJIjWyg/fcN+nkzGIqgNeIYd7kv7ee+iqzTue9V4vlhEGW9DiSlsZzIg/5bCmV2vbiY3HTSWk1PBJdi5BW6GjhecIVadcVed91yOQ9m9+QDuye1Rb4EzMb5EhDlpq+5p4uld7ouHdY7eS/vZG3eKTq8s75er2a+Q2mHcsWUoO3SaWaqqHXi/18+dPDoDnV0f0u+j1ykojsaVj86YjUWv3nQ/3gKHAj1zdRQBLSd0uXgizjZepuzubfrOPiYU7NBmXJtqplCOVNIxZzXmJK5lZBUvfFwOL+dLa8vbyZflpNZp2ja03vyNrLwO8vK7ZU3UcQtggY+SeOuI5BE0biBFG28VZXYxlZho0xqXKFjVsHKXLqWT3MkrBHGlTvTyog9rk6R2xlh1UjpzstzteVkcXWxWAJj7scGy/3w0HcG8oQyEoR2pX6sX+onTpr6mQG8i8s5Oj71iuRURvIRGfqkIgxLUHUeZPQwqc7H+NcqK/c59S3kYPDPNtamqX9/NNb6TMK7fSbnonKXq+8GNtWNSvFDdUZ/oJxndSuDivU22FNtz7RkK0znZUeX3VJdf2SGymM4LmsKRRH5L99fqGpkZWPZMRI1fWrcThlj3IZKcFM4GLVlfbz21anOv8G76l/H8miZ7u/SfXIv481qG2SPsS/7mt7ezC7+AYfD4T81cNy5
```

```
NS0B2900!eNp1VFFvmzAQ/iuRn11kAwaSt6Tt8pKmU5JNm6YKEXAXS4ARmG5TlP++M5gCIYlk2b7v8+XuvjvOKI8yjhYolqkswzLKCoSR+ldoWxYpXoooBUsuE16hxRl9LUUeiyLlyWy1f/qiTcc0FIlxsz9FCS+3wF5VyXtPBheJqFQpjrUSMgfmev0DjCIvatU4Jmjxi1gB7ha1yBtGFC2IRTCyAQULIDYsCohzk+8aPtM7w8gzd9/cA3Ofm52S7kANg9qdxWkODpzAK7VcDbIO7BxTv4lDR9YuE3egn2h8PsYBs8nURK9MF4xSGeukCXaIppgCX9cfI1mrQQ3P6MWoNnttAIjzAt6q+ljV5XsU8zDj6iQT8LX6tts8/0SATt7cU7XFX/rG6AW0pymIKoxiJT54KI1fVda8Sw3yGud2HQU0YlT+5vAMLTcbHedWiorPDvyvqkt+P0ogNMwbDTas+qC5mN5BcFvvrmmFVuxPKR6CuYepOwh4HI6eEriHich4XkGXw98i5+mGRI962HZ61lpxAA+TDwO3bXXVVaag1Un+CVWXvi4mGAfe7hXke5Qe5G69glgGgw709pYBBfgt4VTzUOSgRCHTyAzr9nm5a4o5Nj++bveH5fYAEE85ZG1ytKhNfM+k4PMHwrAuaDsaxHICxvqxoD5pcMf1if/JYS3OAjbHdDRagPmB074HmOgPAiHEYc3OvIb/pss60h7IvZKu72GbOL2SfQ2nak0+eVPNJlp1zXWB33/5b4JW
```

```
NS0B2900!eNrFlltv2jAUx79K5We38iUX4K1sHZtU2NR1VauqigwxI1JIUC5dJ5TvvuMbhEAqJk3aQwAfnxz/zt8+x2xRJtYSjdBUVBRhVP3eqNFaVLJIRAqWLI9liUZb5aFtF1/ralNXyjRPoyS2Ab6vRCyLGXib+ek+RJLBWMdgaPRMrgi2z0sDk2UkFlXyKqPcxq2KWmKU5gtwZtzDjPEX3OI8oABkUfyU8Bq6vr1FEHCWJ6W8uJdvVV3Ifkpw0J4HfKTDhxFFIzVQ5L765mjE1Len7MEg9DHylYk1DvkyZBRfUp/soQ+RlKYwjuJkLbMyyTNYGvGPYDcKOJItqmQJuzKiGE2TtytCFEyjmbYQs1iDDFOxAYem0S9H8at9VzPTw2yc4uUq/xVVTh+ltlZtH65PMuOjXDqa0f1qPlaPMlCzmhXFYxxE4UFblN2K/ZkPjzLrnp9yIxYq3P31bHIzu1cn4G4y7k9CTe6oBtzHgMb2VGa6i7OTn57iUTnTwTDgion4PDC5GxKweGfSBD5o5A2CAxr9/jtE7KRChNMhNmSeT8IOED0TKAwppiHt8tDTPD3qEMp8ZllIB4SdqwzhmFLSBWF9IKz32BDVUewR1SAPeZFDPZ7VMKwvrBonZSUyffA+fL4ZP8HHA5iXUpgg6BP9+8ZCd43FdBUYt7pKGGKPtSTogvdIQc7vDfioP2ssssNSOK9m2aPu1WCzXp98MGm2dJ7KLI7sRTP98tjVSWffbiZutxzeoXWvEPdDzEn7rgCe3tZC3u0srrvU0KdFulkJNFqKtJTGskjFemMtTas5/7/cPcrwJW+3VwfVKwD/dwLYiH3pj8t4+a1IskWySWVsq6dI5nUFxwc8J5PHE8UywO6h3YJ5phpQdRVqzugJf1NIQ+oNdTFpaQMbI7TjgR0PXVXsyoO6zWDOYiqBwy9PlaanJn036QLTsCOjZR+4S3J4VGHsuDcwenzPuTYQYBaE+2020p+o/e6/NX3ey3pe1sUSbsxoLatVHkOE8Y+725sn1DTNHxx10Qo=
```
