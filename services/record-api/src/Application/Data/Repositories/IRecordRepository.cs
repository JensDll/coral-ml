using Application.Data.DataTransfer;
using Application.Data.DataTransfer.Record;
using Domain.Entities;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Repositories
{
    public interface IRecordRepository
    {
        public Task<PaginationEnvelope<RecordGetAll>>
            GetWithRecordTypeIdAsync(Pagination pagination, int recordTypeId);

        public Task<RecordGetById> GetByIdAsync(int id);

        public Task<RecordGetLoaded> GetLoadedAsync();

        public Task<byte[]> DownloadAsync(int id);

        public Task<int> CreateAsync(RecordCreate createData);

        public Task<int> SetLoadedAsync(int recordId);

        public Task<int> DeleteAsync(int id);
    }
}
