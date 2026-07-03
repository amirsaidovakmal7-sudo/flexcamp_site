# from amocrm.v2 import tokens
# import os
# print('1. Запуск')
#
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(f"Сохраняем токены в: {BASE_DIR}")
#
#
# tokens.default_token_manager(
#     client_id="e9a129fe-7c84-4f9e-9bbc-5ce01612a78c",
#     client_secret="6VtBvucwQAGGnmqCB5z9W1JNztfLky0IOe7fq4Um0UUFGWBT81MEc0jTikQbuxok",
#     subdomain="muslimpulatov0317",
#     redirect_url="https://flexcamp.uz",
#     storage=tokens.FileTokensStorage(directory_path=BASE_DIR),  # by default FileTokensStorage
# )
#
#
# print("2. Менеджер настроен")
#
# try:
#     tokens.default_token_manager.init(code="def50200611661ddc8508f5e22b93ebd6869d063daa3a5729adfcfd61d1868a865f2da7276383798bcc8728c067f2de9e1b683ef8d3277949adcf89cc27698c3e2512641989c984676434f2fb92a873e121ae8563edce81281e8a7c07f5042bed376ec2acb274b0e85204ff9d9cb4c37c3298954b518f5a3be32124bb6a1417ffb7e8b33af03ba74295194f525fc1f1c7c257310415c1272dd08ca42c595776ade7a89f270271a042c34e40cdaa776dc1e1968e17ec4da35c6671537a3cc3ff35890b081f35c1f654d31aeee1c2560d25e2e0d678ecace4675ce892d9b533f87ad0e4c147491cefc91552520bffe0f2fde6b21d967c7011c43b5e720c2cdab06e5dcecaa69c4bfdca302225c8bf475b5b693e43889a56bcee6dde0e046fa8884704cd3b3355f01bba0a64f02585087498d77853a9122396c65f33765093a009243328fbda395565f4f1ac939736b9877cb855ff8efb63211d36b7a747ce0607d6fa7b835f52bf23d9d9930a79a21b4c0b512c5c1a4ba2156d20a8ecc34ede02f3e81235db1ea25e12d0aa71a02406ea8aaef2adab2835b8713469106f0c9e05393702e665c9919410523103c09948b666723e0539ae899255719e6ecf32656ed28377e3388dd92bef776bb24dd412cbaf85bcea311a8366398c1bd2b93a906f569179e74 ", skip_error=False)
#     print('3. Успешно')
# except Exception as e:
#     print(f'Ошибка {e}')