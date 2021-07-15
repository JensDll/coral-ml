using Application.Data;
using Application.Data.Repositories;
using Application.Mapping.Record;
using Infrastructure.Data;
using Infrastructure.Data.Repositories;
using Infrastructure.Mapping.Record;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Infrastructure
{
    public static class DependencyInjection
    {
        public static void AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
        {
            // data access
            services.AddSingleton<IConnectionFactory>
                (new ConnectionFactory(configuration.GetConnectionString("RecordDbMaria")));
            services.AddSingleton<IRecordRepository, RecordRepository>();
            services.AddSingleton<IRecordTypeRepository, RecordTypeRepository>();

            // mapping
            services.AddSingleton<IRecordRequestMapper, RecordRequestMapper>();
        }
    }
}
