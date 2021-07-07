using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Dapper;
using Contracts;
using System.Data;
using System.IO;
using Domain.Entities;
using Application.Data;
using Application.Data.Repositories;
using Application.Data.Models;

namespace Infrastructure.Data.Repositories
{
    internal class ModelRepository : IModelRepository
    {
        private readonly IConnectionFactory _connectionFactory;

        public ModelRepository(IConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public Task<byte[]> GetAll()
        {
            throw new NotImplementedException();
        }

        public async Task<TFLiteModelModel> GetById(int id)
        {
            using var cnn = _connectionFactory.NewConnection;

            return await cnn.QuerySingleAsync<TFLiteModelModel>(StoredProcedures.Model.GetById,
                param: new { id },
                commandType: CommandType.StoredProcedure);
        }

        public async Task<int> Save(IFormFile modelFile)
        {
            using var cnn = _connectionFactory.NewConnection;
            using var memoryStream = new MemoryStream();

            await modelFile.CopyToAsync(memoryStream);

            return await cnn.QuerySingleAsync<int>(StoredProcedures.Model.Save,
                param: new { modelName = modelFile.FileName, model = memoryStream.ToArray() },
                commandType: CommandType.StoredProcedure);
        }
    }
}
