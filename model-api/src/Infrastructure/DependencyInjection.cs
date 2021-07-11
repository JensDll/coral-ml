using Application.Data;
using Application.Data.Repositories;
using Application.Mapping.Model;
using Infrastructure.Data;
using Infrastructure.Data.Repositories;
using Infrastructure.Mapping.Model;
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
                (new ConnectionFactory(configuration.GetConnectionString("ModelDb")));
            services.AddSingleton<ITFLiteRecordRepository, TFLiteRecordRepository>();

            // mapping
            services.AddSingleton<ITFLiteRecordRequestMapper, TFLiteRecordRequestMapper>();
            services.AddSingleton<ITFLiteRecordResponseMapper, TFLiteRecordResponseMapper>();
        }
    }
}
