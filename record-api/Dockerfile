FROM mcr.microsoft.com/dotnet/sdk:5.0 as build
WORKDIR /source

# copy csproj and restore as distinct layers
COPY src/Application/*.csproj ./Application/
COPY src/Contracts/*.csproj ./Contracts/
COPY src/Domain/*.csproj ./Domain/
COPY src/Infrastructure/*.csproj ./Infrastructure/
COPY src/RecordAPI/*.csproj ./RecordAPI/

RUN dotnet restore RecordAPI/RecordAPI.csproj

# copy everything else and build
COPY src/Application ./Application/
COPY src/Contracts ./Contracts/
COPY src/Domain ./Domain/
COPY src/Infrastructure ./Infrastructure/
COPY src/RecordAPI ./RecordAPI/

WORKDIR /source/RecordAPI
RUN dotnet build -c release --no-restore

FROM build AS publish
RUN dotnet publish -c release --no-build -o /app

# final image
FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app
COPY --from=publish /app ./
EXPOSE 80
ENTRYPOINT ["dotnet", "RecordAPI.dll"]